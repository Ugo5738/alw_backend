import asyncio
import json
import logging
import os
import time
import uuid
from datetime import datetime

import openai
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from dotenv import load_dotenv

from accounts.models import OrganizationCustomer
from assistant.knowledge import query_vec_database
from assistant.memory import KnowledgeBaseMemory
from assistant.models import Channel, Conversation, Message, MessageVote
from assistant.tasks import save_learn_conversation
from helpers import learn_utils

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LearnChatConsumer(AsyncWebsocketConsumer):
    """
        LearnChatConsumer handles WebSocket connections for chat rooms, managing user messages,
        chatbot responses, and conversation state.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversation_tracker = KnowledgeBaseMemory()

    async def connect(self):
        """
            Handles a new WebSocket connection, joining the user to the appropriate chat room,
            and initializing the conversation state.
        """
        logger.info("---------- LEARN CONNECTION ATTEMPT RECEIVED ----------")
        
        # Generate a unique ID for the conversation
        self.room_name = str(uuid.uuid4())
        self.room_group_name = f'chat_{self.room_name}'

        self.conversation_memory = KnowledgeBaseMemory()

        # Create the Conversation instance without setting the customer and channel
        self.conversation = await database_sync_to_async(Conversation.objects.create)()

        # Initialize the conversation start time
        self.conversation_memory.session_start_time = datetime.now()
        logger.info(f"Conversation start time: {self.conversation_memory.session_start_time}")

        # Send message to room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        logger.info("---------- LEARN CONNECTION DISCONNECTED ----------")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        logger.info("---------- LEARN MESSAGE RECEIVED ----------")
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        try:
            logger.info(f"MESSAGE TYPE: {message_type}")

            if message_type == 'user_message':

                start = time.time()
                self.user_id = text_data_json.get('userId')
                user_message = text_data_json.get('message')
                message_id = str(uuid.uuid4())

                context1, context2= await query_vec_database(query=user_message, num_results=2, pinecone_index_name="clarify")
                context = context1['metadata']['text'] + "\n\n" + context2['metadata']['text']

                # if we want to store this data in the database (connect it to message id)
                # context_text_1, context_score_1 = context1['metadata']['text'], context1['score']
                # context_text_2, context_score_2 = context2['metadata']['text'], context2['score']
                # context_text_3, context_score_3 = context3['metadata']['text'], context3['score']

                # build our prompt with the retrieved contexts included
                prompt_start = ("Answer the question based on the context below.\n\n" + "Context:\n")
                prompt_end = (f"\n\nQuestion: {user_message}\nAnswer:")
                user_ques = (prompt_start + "\n\n---\n\n" + context + prompt_end)
                
                self.conversation_tracker.add_message(role='user', content=user_ques, message_id=message_id)

                bot_response = await self.generate_bot_response(user_ques)
                # logger.info(bot_response)

                stop = time.time()
                duration = stop - start
                
                # Add to the conversation tracker
                response_id = str(uuid.uuid4())
                self.conversation_tracker.add_message(role='assistant', content=bot_response, duration=duration, message_id=response_id)
                
                logger.info(f"LEARN RESPONSE DURATION: {duration}")

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': bot_response, 
                        'messageId': message_id
                    }
                )

            elif message_type == 'upvote':
                message_id = text_data_json.get('messageId')
                logger.info(f"MESSAGE {message_id} UPVOTED!")
                self.conversation_tracker.upvote(message_id)

            elif message_type == 'downvote':
                message_id = text_data_json.get('messageId')
                logger.info(f"MESSAGE {message_id} DOWNVOTED!")
                self.conversation_tracker.downvote(message_id)
            
            elif message_type == 'end_session':
                logger.info("SESSION END")

                await self.end_learn_conversation()
            
                await self.close()

        except json.JSONDecodeError:
            logger.error("Received invalid JSON data")
            return
        except Exception as e:
            logger.error(f"An unexpected error occurred while processing the received data: {str(e)}")
            return

    # Receive message from room group
    async def chat_message(self, event):
        """
        Receives a message from the room group and sends it to the WebSocket.
        """
        logger.info("---------- FORWARDING BOT MESSAGE ----------")

        message = event.get('message')  
        message_id = event.get('messageId')    

        json_message = json.dumps({
            'message': message,
            'messageId': message_id
        })    

        logger.info(f"LEARN MESSAGE TO WEBSOCKET: ")
        logger.info(f"{json_message}")

        # Send message to WebSocket
        await self.send(text_data=json_message)

    # ----------------------- CUSTOM ASYNC FUNCTIONS --------------------------
    async def generate_bot_response(self, user_message):
        logger.info("---------- BOT ENGINE STARTED ----------")

        full_history = self.conversation_tracker.get_openai_history()

        logger.info(f"CONVERSATION MEMORY: ")
        logger.info(full_history)

        # Make a copy and remove the most recent message (presumably the user's latest question)
        history_except_last = full_history[:-1]  # RECTIFY: this should be the latest context not latest question
        
        messages1 = [
            {
                "role": "system",
                "content": learn_utils.SYSTEM_INSTRUCTION
            },
            *full_history
        ]

        messages2 = [
            {
                "role": "system",
                "content": learn_utils.SYSTEM_INSTRUCTION_2
            },
            *history_except_last,
        ]

        response1, response2 = await asyncio.gather(
            learn_utils.single_bot_query(messages1),
            learn_utils.single_bot_query(messages2)
        )

        # Separate the main answer from the confidence level
        answer1, confidence_level1 = await learn_utils.separate_confidence_from_answer(response1)

        # Separate the main answer from the confidence level
        answer2, confidence_level2 = await learn_utils.separate_confidence_from_answer(response2)

        final_response = answer1

        # need to debug this
        # Checking responses
        # if "The context is insufficient" in answer2 or "0%" in confidence_level2:
        #     final_response = answer1
        # else:
        #     final_response = answer2  # Or check for confidence level here before deciding

        if final_response:
            final_response = final_response.replace("\n", "<br>")
        
        logger.info("---------- BOT ENGINE STOPPED ----------")
        return final_response
    
    async def end_learn_conversation(self):
        # self.conversation = await database_sync_to_async(Conversation.objects.create)()
        self.conversation_tracker.session_end_time = datetime.now()

        conversation_tracker_dict = self.conversation_tracker.to_dict()
        
        save_learn_conversation.apply_async(args=[conversation_tracker_dict, str(self.conversation.id), "learn"])
        
        return "Done!"
    # ----------------------- CUSTOM ASYNC FUNCTIONS --------------------------
