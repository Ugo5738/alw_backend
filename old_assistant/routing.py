from django.urls import path

from assistant import consumers

websocket_urlpatterns = [
    path('ws/chat/learn/', consumers.LearnChatConsumer.as_asgi()),
]
