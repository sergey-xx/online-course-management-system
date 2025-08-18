from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import HelloWorld, CourseViewSet

router = DefaultRouter()

router.register('courses',
                CourseViewSet,
                basename='courses')

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('', HelloWorld.as_view()),
    path('', include(router.urls)),
]
