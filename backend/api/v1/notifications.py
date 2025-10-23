from api.v1.constants import ChannelGroup
from courses.models import Comment, Course, Grade, HomeWork, Lecture, Submission
from courses.serializers import (CommentSerializer, CourseSerializer, GradeSerializer, HomeWorkSerializer,
                                 LectureSerializer, SubmissionSerializer)
from project.notifications import NotificationSender


class NotificationSenderV1(NotificationSender):

    group = ChannelGroup.NOTIFICATION

    serializers_map = {
        Course: CourseSerializer,
        Lecture: LectureSerializer,
        HomeWork: HomeWorkSerializer,
        Submission: SubmissionSerializer,
        Grade: GradeSerializer,
        Comment: CommentSerializer,
    }
