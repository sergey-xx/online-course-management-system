from dataclasses import dataclass

from rest_framework import serializers


@dataclass
class Message:

    text: str


class MessageSerializer(serializers.Serializer):

    text = serializers.CharField()
