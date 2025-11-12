from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .docs import NotificationWebSocketDocsView
from .views import (
    CommentViewSet,
    CourseViewSet,
    GradeViewSet,
    HomeWorkSubmissionViewSet,
    LectureHomeWorkViewSet,
    LectureViewSet,
    MyHomeWorkViewSet,
)

router = DefaultRouter()

router.register("courses", CourseViewSet, basename="courses")

router.register(r"courses/(?P<course_id>\d+)/lectures", LectureViewSet, basename="course-lectures")

router.register(r"lectures/(?P<lecture_id>\d+)/homeworks", LectureHomeWorkViewSet, basename="lecture-homeworks")

router.register(
    r"homeworks/(?P<homework_id>\d+)/submissions", HomeWorkSubmissionViewSet, basename="homework-submissions"
)

router.register(r"submissions/grade/(?P<grade_id>\d+)/comments", CommentViewSet, basename="submission-submissions")

router.register(r"my/homeworks", MyHomeWorkViewSet, basename="my-homeworks")

urlpatterns = [
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.jwt")),
    path(
        "submissions/<int:submission_id>/grade/",
        GradeViewSet.as_view(
            {
                "post": "create",
                "patch": "partial_update",
            }
        ),
        name="submission-grade",
    ),
    path("", include(router.urls)),
    path("notifications/", NotificationWebSocketDocsView.as_view(), name="ws"),
]
