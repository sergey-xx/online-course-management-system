import json
import uuid
from dataclasses import dataclass, field

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Model
from rest_framework.renderers import JSONRenderer

from courses.models import Comment, Course, Grade, HomeWork, Lecture, Submission
from courses.serializers import (CommentSerializers, CourseSerializers, GradeSerializers, HomeWorkSerializers,
                                 LectureSerializers, SubmissionSerializers)
from project.constants import EventEnum

channel_layer = get_channel_layer()

serializers_map = {
    Course: CourseSerializers,
    Lecture: LectureSerializers,
    HomeWork: HomeWorkSerializers,
    Submission: SubmissionSerializers,
    Grade: GradeSerializers,
    Comment: CommentSerializers,
}

object_names = {
    Course: 'course'
}


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


def object_to_dict(instance: Model):
    serializer_class = serializers_map[type(instance)]
    serializer = serializer_class(instance)
    json_string = JSONRenderer().render(serializer.data).decode('utf-8')
    return json.loads(json_string)


def send_object_to_group(group: str, event: EventEnum, instance: Model):
    obj = object_to_dict(instance)
    object_name = object_names.get(type(instance), 'unknown')
    notification = Notification(
        event=event, object_name=object_name, obj=obj
    )
    json_string = json.dumps(notification.to_dict())
    send_to_group(group, json_string)


def send_to_group(group: str, message: str):
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'get.message',
            'message': message,
        }
    )
