from django.urls import path

from api.v1 import consumers

websocket_urlpatterns = [
    path('notification/', consumers.NotificationConsumer.as_asgi()),
]
