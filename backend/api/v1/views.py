from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import MessageSerializer, Message


class HelloWorld(APIView):

    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={200: MessageSerializer},
    )
    def get(self, request, format=None):
        """
        Return a Hello World message.
        """
        ser = MessageSerializer(Message(text='Hello!'))
        return Response(ser.data)
