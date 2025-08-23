from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins

from courses.models import Course, Grade, HomeWork, Lecture, Submission
from courses.serializers import (CommentSerializers, CourseSerializers,
                                 GradeSerializers, HomeWorkSerializers,
                                 LectureSerializers, MyHomeWorkSerializers,
                                 SubmissionSerializers)

from .filters import HomeWorkFilter
from .permissions import (CanAddHomeWork, CanAddLecture, CanAddReadComment,
                          IsStudentrOrReadOnly, IsTeaacherOrReadOnly,
                          get_owner_permission_class)


class CourseViewSet(ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeaacherOrReadOnly,
        get_owner_permission_class('author')
    ]
    queryset = Course.objects.prefetch_related('teachers', 'students')
    serializer_class = CourseSerializers
    http_method_names = ['get', 'post', 'patch', 'delete']

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
    http_method_names = ['get', 'post', 'patch', 'delete']

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
    http_method_names = ['get', 'post', 'patch', 'delete']

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
    http_method_names = ['get', 'post', 'patch', 'delete']

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
    lookup_field = 'submission_id'
    queryset = Grade.objects.all()
    http_method_names = ['post', 'patch']

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
        if self.request.user.role == 'TEACHER':
            return (
                super().get_queryset()
                .filter(author=self.request.user)
                .prefetch_related('submissions'))
        return (
            super()
            .get_queryset()
            .filter(lecture__course__students=self.request.user)
            .prefetch_related(Prefetch('submissions', Submission.objects.filter(author=self.request.user)))
        )


class CommentViewSet(ModelViewSet):
    """
    ViewSet for comments.
    """
    permission_classes = [
        permissions.IsAuthenticated,
        CanAddReadComment,
        get_owner_permission_class('author')
    ]
    serializer_class = CommentSerializers
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        grade_id = self.kwargs.get('grade_id')
        if self.request.user.role == 'TEACHER':
            grade = get_object_or_404(Grade, pk=grade_id)
        else:
            grade = get_object_or_404(Grade, pk=grade_id, submission__author=self.request.user)
        return grade.comments.all()

    def perform_create(self, serializer):
        grade_id = self.kwargs.get('grade_id')
        grade = get_object_or_404(Grade, pk=grade_id)
        serializer.save(grade=grade, author=self.request.user)
