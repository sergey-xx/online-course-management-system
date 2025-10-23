from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from project.constants import EventEnum

from .notifications import NotificationSenderV1


class ClientWebSocketMessageSerializer(serializers.Serializer):
    """Сообщение, которое клиент отправляет на сервер."""
    command = serializers.ChoiceField(choices=['subscribe', 'send_message'])
    room = serializers.CharField(max_length=100, required=False)
    message = serializers.CharField(required=False)


class ServerWebSocketMessageSerializer(serializers.Serializer):
    """Сообщение, которое сервер отправляет клиенту."""
    id = serializers.UUIDField()
    event = serializers.ChoiceField(choices=[value for value in EventEnum])
    object_name = serializers.ChoiceField(
        choices=[klass.Meta.api_object_name for klass in NotificationSenderV1.serializers_map.values()]
    )
    obj = serializers.DictField()


class NotificationWebSocketDocsView(APIView):
    """
    A dummy view for WebSocket documentation.
    This view doesn't handle real requests.
    """

    @extend_schema(
        responses={
            200: ServerWebSocketMessageSerializer
        },
        tags=["WebSockets (Chat)"],
        summary="Connect to notification service by WebSocket",
        description="""
        This endpoint establishes a WebSocket connection for chat.
        Protocol: `ws://` or `wss://`
        ---
    """
    )
    def get(self, request, *args, **kwargs):
        """
        This method will not be called. It is only needed for documentation.
        """
        return Response(status=501, data={"detail": "This is a WebSocket endpoint. Use ws:// protocol."})
