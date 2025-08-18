from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment, Course, HomeWork, Lecture, Submission

User = get_user_model()


class CommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'author',
            'created_at',
            'updated_at',
        )


class CourseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'author',
            'teachers',
            'students',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'author',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'teachers': {'required': False},
            'students': {'required': False},
        }


class HomeWorkSerializers(serializers.ModelSerializer):

    class Meta:
        model = HomeWork
        fields = (
            'id',
            'text',
            'lecture',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )


class LectureSerializers(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = (
            'id',
            'course',
            'topic',
            'presentation_file',
            'datetime',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )


class SubmissionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = (
            'id',
            'text',
            'student',
            'homework',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'student',
            'created_at',
            'updated_at',
        )
