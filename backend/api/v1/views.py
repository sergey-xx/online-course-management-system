from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination

from courses.models import Course
from courses.serializers import CourseSerializers

from .serializers import MessageSerializer, Message


class HelloWorld(APIView):

    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={200: MessageSerializer},
    )
    def get(self, request, format=None):
        """
        Return a Hello World message.
        """
        ser = MessageSerializer(Message(text='Hello!'))
        return Response(ser.data)


class CourseViewSet(ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = CourseSerializers

    def perform_create(self, serializer):
        """Set the user who created the course as the author."""
        serializer.save(author=self.request.user)
