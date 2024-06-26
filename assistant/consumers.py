import json
import logging
import time
import uuid
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from accounts.models import User
from alignworkengine.configs.logging_config import configure_logger
from assistant.engine import OpenAIChatEngine
from assistant.memory import BaseMemory
from assistant.tasks import save_conversation

logger = configure_logger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """
    ChatConsumer handles WebSocket connections for chat rooms, managing user messages,
    chatbot responses, and conversation state.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_engine = OpenAIChatEngine(
            api_key=settings.OPENAI_API_KEY, assistant_id=settings.ASSISTANT_ID
        )

    async def connect(self):
        """
        Handles a new WebSocket connection, joining the user to the appropriate chat room,
        and initializing the conversation state.
        """
        logger.info("---------- CONNECTION ATTEMPT RECEIVED ----------")

        # Generate a unique ID for the conversation
        self.room_name = str(uuid.uuid4())
        self.room_group_name = f"chat_{self.room_name}"

        self.conversation_memory = BaseMemory()

        # Start a new conversation thread
        self.thread_id = await self.chat_engine.create_thread()

        self.conversation_memory.session_start_time = datetime.now()
        logger.info(
            f"Conversation start time: {self.conversation_memory.session_start_time}"
        )

        # Send message to room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.info("---------- CONNECTION DISCONNECTED ----------")

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info("---------- MESSAGE RECEIVED ----------")

        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")

        try:
            logger.info(f"MESSAGE TYPE: {message_type}")

            if message_type == "user_message":
                start = time.time()
                # self.user_id = text_data_json.get('userId')
                user_message = text_data_json.get("message")

                # self.user = await database_sync_to_async(User.objects.get)(id=self.user_id)

                response = "message"

                stop = time.time()
                duration = stop - start

                logger.info(f"RESPONSE DURATION: {duration}")

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": response,
                        "messageId": message_id,
                    },
                )

            elif message_type == "upvote":
                message_id = text_data_json.get("messageId")
                self.conversation_memory.upvote(message_id)
                logger.info(f"MESSAGE {message_id} UPVOTED!")

            elif message_type == "downvote":
                message_id = text_data_json.get("messageId")
                self.conversation_memory.downvote(message_id)
                logger.info(f"MESSAGE {message_id} DOWNVOTED!")

            elif message_type == "end_session":
                self.username_id = text_data_json.get("userId")

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": "session_ended",
                    },
                )

        except json.JSONDecodeError:
            logger.error("Received invalid JSON data")
            return
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while processing the received data: {str(e)}"
            )
            return

    # Receive message from room group
    async def chat_message(self, event):
        """
        Receives a message from the room group and sends it to the WebSocket.
        """
        logger.info("---------- FORWARDING BOT MESSAGE ----------")

        message = event.get("message")
        message_id = event.get("messageId")

        json_message = json.dumps({"message": message, "messageId": message_id})

        logger.info(f"MESSAGE TO WEBSOCKET: ")
        logger.info(f"{json_message}")

        # Send message to WebSocket
        await self.send(text_data=json_message)

        return "Done!"
