import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Model
from rest_framework.renderers import JSONRenderer

from courses.models import Comment, Course, Grade, HomeWork, Lecture, Submission
from courses.serializers import (CommentSerializers, CourseSerializers, GradeSerializers, HomeWorkSerializers,
                                 LectureSerializers, SubmissionSerializers)

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


def serialize_object(instance: Model):
    serializer_class = serializers_map[type(instance)]
    serializer = serializer_class(instance)
    json_string = JSONRenderer().render(serializer.data).decode('utf-8')
    return json_string


def send_object_to_group(group: str, instance: Model):
    message = serialize_object(instance)
    name = object_names.get(type(instance), 'unknown')
    json_string = json.dumps({name: json.loads(message)})
    send_to_group(group, json_string)


def send_to_group(group: str, message: str):
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'get.message',
            'message': message,
        }
    )
