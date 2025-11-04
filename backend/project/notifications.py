import json
import uuid
from dataclasses import dataclass, field

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Model
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import Serializer

from project.constants import ChannelGroup, EventEnum

channel_layer = get_channel_layer()


@dataclass
class Notification:

    event: EventEnum | str
    object_name: str
    obj: dict
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def to_dict(self):
        return {
            'id': str(self.id),
            'event': self.event,
            'object_name': self.object_name,
            'obj': self.obj
        }


@dataclass
class NotificationSender:
    group = ChannelGroup.NOTIFICATION

    instance: Model
    event: EventEnum
    serializer_class: type[Serializer] | None = None

    @property
    def serializer(self):
        if self.serializer_class:
            return self.serializer_class(self.instance)
        return self.serializers_map[type(self.instance)](self.instance)

    def to_dict(self):
        json_string = JSONRenderer().render(self.serializer.data).decode('utf-8')
        return json.loads(json_string)

    def send(self):
        obj = self.to_dict()
        notification = Notification(
            event=self.event, object_name=self.serializer.Meta.api_object_name, obj=obj
        )
        json_string = json.dumps(notification.to_dict())
        async_to_sync(channel_layer.group_send)(
            self.group, {
                'type': 'get.message',
                'message': json_string,
            }
        )
