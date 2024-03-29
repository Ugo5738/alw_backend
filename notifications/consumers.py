import json
import time
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer

from alignworkengine.configs.logging_config import configure_logger

logger = configure_logger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    NotificationConsumer handles WebSocket connections for chat rooms, managing user messages,
    notification responses, and conversation state.
    """

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.chat_engine = OpenAIChatEngine(
    #         api_key=settings.OPENAI_API_KEY, assistant_id=settings.ASSISTANT_ID
    #     )

    async def connect(self):
        """
        Handles a new WebSocket connection, joining the user to the appropriate chat room,
        and initializing the conversation state.
        """
        logger.info("---------- CONNECTION ATTEMPT RECEIVED ----------")

        # Generate a unique ID for the conversation
        self.room_name = str(uuid.uuid4())
        self.room_group_name = f"chat_{self.room_name}"

        # Send message to room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.info("---------- CONNECTION DISCONNECTED ----------")

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
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

    # Custom handler for sending notifications, called from elsewhere in Django
    async def send_notification(self, event):
        """
        Receives a message from the room group and sends it to the WebSocket.
        """
        logger.info("---------- FORWARDING NOTIFICATION DETAILS ----------")

        message = event.get("message")

        json_message = json.dumps({"message": message})

        logger.info(f"MESSAGE TO WEBSOCKET: ")
        logger.info(f"{json_message}")

        # Send message to WebSocket
        await self.send(text_data=json_message)

        return "Done!"
