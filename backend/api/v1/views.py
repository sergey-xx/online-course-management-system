from courses.models import Course, Lecture, HomeWork, Grade, Submission
from courses.serializers import (CourseSerializers, HomeWorkSerializers,
                                 LectureSerializers, SubmissionSerializers,
                                 MyHomeWorkSerializers, CommentSerializers, GradeSerializers)
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .filters import HomeWorkFilter
from .permissions import (CanAddHomeWork, CanAddLecture, IsTeaacher, IsTeaacherOrReadOnly,
                          IsStudentrOrReadOnly, get_owner_permission_class)


class CourseViewSet(ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeaacher,
        get_owner_permission_class('author')
    ]
    queryset = Course.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = CourseSerializers

    def perform_create(self, serializer):
        """Set the user who created the course as the author."""
        serializer.save(author=self.request.user)


class LectureViewSet(ModelViewSet):
    """
    ViewSet for lectures. multipart/form-data
    """
    permission_classes = [
        permissions.IsAuthenticated,
        IsTeaacherOrReadOnly,
        CanAddLecture,
    ]
    serializer_class = LectureSerializers
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        return course.lectures.all()

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        serializer.save(course=course)


class LectureHomeWorkViewSet(ModelViewSet):
    """
    ViewSet for homeworks.
    """
    permission_classes = [
        permissions.IsAuthenticated,
        IsTeaacherOrReadOnly,
        CanAddHomeWork,
        get_owner_permission_class('author')
    ]
    serializer_class = HomeWorkSerializers

    def get_queryset(self):
        lecture_id = self.kwargs.get('lecture_id')
        lecture = get_object_or_404(Lecture, id=lecture_id)
        return lecture.homeworks.all()

    def perform_create(self, serializer):
        lecture_id = self.kwargs.get('lecture_id')
        lecture = get_object_or_404(Lecture, id=lecture_id)
        serializer.save(lecture=lecture, author=self.request.user)


class HomeWorkSubmissionViewSet(ModelViewSet):
    """
    ViewSet for submissions.
    """
    permission_classes = [
        permissions.IsAuthenticated,
        IsStudentrOrReadOnly,
        get_owner_permission_class('author')
    ]
    serializer_class = SubmissionSerializers

    def get_queryset(self):
        homework_id = self.kwargs.get('homework_id')
        homework = get_object_or_404(HomeWork, id=homework_id)
        queryset = homework.submissions.select_related('grade')
        if self.request.user.role == 'TEACHER':
            return queryset.all()
        return queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        homework_id = self.kwargs.get('homework_id')
        homework = get_object_or_404(HomeWork, id=homework_id)
        serializer.save(homework=homework, author=self.request.user)


class GradeViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    """
    ViewSet for creating/changing grades.
    """
    permission_classes = [
        permissions.IsAuthenticated,
        IsTeaacherOrReadOnly,
        get_owner_permission_class('author')
    ]
    serializer_class = GradeSerializers

    def perform_create(self, serializer):
        submission_id = self.kwargs.get('submission_id')
        submission = get_object_or_404(Submission, id=submission_id)
        serializer.save(submission=submission, author=self.request.user)


class MyHomeWorkViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """
    ViewSet for my homeworks.
    """
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = MyHomeWorkSerializers
    queryset = HomeWork.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HomeWorkFilter

    def get_queryset(self):
        return super().get_queryset().filter(lecture__course__students=self.request.user)


class CommentViewSet(ModelViewSet):
    """
    ViewSet for comments.
    """
    permission_classes = [
        permissions.IsAuthenticated,
        get_owner_permission_class('author')
    ]
    serializer_class = CommentSerializers

    def get_queryset(self):
        grade_id = self.kwargs.get('grade_id')
        grade = get_object_or_404(Grade, submission_id=grade_id)
        return grade.comments.all()

    def perform_create(self, serializer):
        homework_id = self.kwargs.get('homework_id')
        homework = get_object_or_404(HomeWork, id=homework_id)
        serializer.save(homework=homework, author=self.request.user)
