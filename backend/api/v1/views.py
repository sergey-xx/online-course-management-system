from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins

from core.views import SearchViewMixin, ServiceViewMixin
from courses.documents import CourseDocument
from courses.models import Course, Grade, HomeWork, Lecture, Submission
from courses.serializers import (
    CommentSerializer,
    CourseSerializer,
    GradeSerializer,
    HomeWorkSerializer,
    LectureSerializer,
    MyHomeWorkSerializer,
    SubmissionSerializer,
)
from courses.services import (
    CommentService,
    CourseService,
    GradingService,
    HomeWorkService,
    LectureService,
    SubmissionService,
)

from .filters import HomeWorkFilter
from .permissions import (
    CanAddHomeWork,
    CanAddLecture,
    CanAddReadComment,
    IsStudentrOrReadOnly,
    IsTeaacherOrReadOnly,
    get_owner_permission_class,
)


class CourseViewSet(ServiceViewMixin, SearchViewMixin, ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsTeaacherOrReadOnly, get_owner_permission_class("author"))
    queryset = Course.objects.prefetch_related("teachers", "students")
    serializer_class = CourseSerializer
    http_method_names = ("get", "post", "patch", "delete")
    service_class = CourseService
    document_class = CourseDocument
    search_fields = ("title",)


class LectureViewSet(ServiceViewMixin, ModelViewSet):
    """ViewSet for lectures. multipart/form-data."""

    permission_classes = (
        permissions.IsAuthenticated,
        IsTeaacherOrReadOnly,
        CanAddLecture,
    )
    serializer_class = LectureSerializer
    parser_classes = (MultiPartParser,)
    http_method_names = ("get", "post", "patch", "delete")
    service_class = LectureService

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        return course.lectures.all()

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        service = self.get_service()
        serializer.instance = service.create(course=course, **serializer.validated_data)


class LectureHomeWorkViewSet(ServiceViewMixin, ModelViewSet):
    """ViewSet for homeworks."""

    permission_classes = (
        permissions.IsAuthenticated,
        IsTeaacherOrReadOnly,
        CanAddHomeWork,
        get_owner_permission_class("author"),
    )
    serializer_class = HomeWorkSerializer
    http_method_names = ("get", "post", "patch", "delete")
    service_class = HomeWorkService

    def get_queryset(self):
        lecture_id = self.kwargs.get("lecture_id")
        lecture = get_object_or_404(Lecture, id=lecture_id)
        return lecture.homeworks.all()

    def perform_create(self, serializer):
        lecture_id = self.kwargs.get("lecture_id")
        lecture = get_object_or_404(Lecture, id=lecture_id)
        service = self.get_service()
        serializer.instance = service.create(lecture=lecture, **serializer.validated_data)


class HomeWorkSubmissionViewSet(ServiceViewMixin, ModelViewSet):
    """ViewSet for submissions."""

    permission_classes = (permissions.IsAuthenticated, IsStudentrOrReadOnly, get_owner_permission_class("author"))
    serializer_class = SubmissionSerializer
    http_method_names = ("get", "post", "patch", "delete")
    service_class = SubmissionService

    def get_queryset(self):
        homework_id = self.kwargs.get("homework_id")
        homework = get_object_or_404(HomeWork, id=homework_id)
        queryset = homework.submissions.select_related("grade")
        if self.request.user.role == "TEACHER":
            return queryset.all()
        return queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        homework_id = self.kwargs.get("homework_id")
        homework = get_object_or_404(HomeWork, id=homework_id)
        service = self.get_service()
        serializer.instance = service.create(homework=homework, **serializer.validated_data)


class GradeViewSet(ServiceViewMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """ViewSet for creating/changing grades."""

    permission_classes = (permissions.IsAuthenticated, IsTeaacherOrReadOnly, get_owner_permission_class("author"))
    serializer_class = GradeSerializer
    lookup_field = "submission_id"
    queryset = Grade.objects.all()
    http_method_names = ("post", "patch")
    service_class = GradingService

    def perform_create(self, serializer):
        submission_id = self.kwargs.get("submission_id")
        submission = get_object_or_404(Submission, id=submission_id)
        grading_service = self.get_service()
        grading_service.create(
            submission=submission,
            score=serializer.validated_data["score"],
        )


class MyHomeWorkViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """ViewSet for my homeworks."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MyHomeWorkSerializer
    queryset = HomeWork.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HomeWorkFilter

    def get_queryset(self):
        if self.request.user.role == "TEACHER":
            return super().get_queryset().filter(author=self.request.user).prefetch_related("submissions")
        return (
            super()
            .get_queryset()
            .filter(lecture__course__students=self.request.user)
            .prefetch_related(Prefetch("submissions", Submission.objects.filter(author=self.request.user)))
        )


class CommentViewSet(ServiceViewMixin, ModelViewSet):
    """ViewSet for comments."""

    permission_classes = (permissions.IsAuthenticated, CanAddReadComment, get_owner_permission_class("author"))
    serializer_class = CommentSerializer
    http_method_names = ("get", "post", "patch", "delete")
    service_class = CommentService

    def get_queryset(self):
        grade_id = self.kwargs.get("grade_id")
        if self.request.user.role == "TEACHER":
            grade = get_object_or_404(Grade, pk=grade_id)
        else:
            grade = get_object_or_404(Grade, pk=grade_id, submission__author=self.request.user)
        return grade.comments.all()

    def perform_create(self, serializer):
        grade_id = self.kwargs.get("grade_id")
        grade = get_object_or_404(Grade, pk=grade_id)
        service = self.get_service()
        serializer.instance = service.create(grade=grade, **serializer.validated_data)
