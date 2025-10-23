from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment, Course, Grade, HomeWork, Lecture, Submission

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        api_object_name = 'comment'
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


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        api_object_name = 'course'
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
            'teachers': {'required': False, 'allow_empty': True},
            'students': {'required': False, 'allow_empty': True},
        }


class LectureSerializer(serializers.ModelSerializer):

    class Meta:
        api_object_name = 'lecture'
        model = Lecture
        fields = (
            'id',
            'course',
            'topic',
            'teacher',
            'presentation_file',
            'datetime',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'course',
            'created_at',
            'updated_at',
        )


class GradeSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='submission_id', read_only=True)

    class Meta:
        api_object_name = 'grade'
        model = Grade
        fields = (
            'id',
            'score',
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


class SubmissionSerializer(serializers.ModelSerializer):

    grade = GradeSerializer(read_only=True)

    class Meta:
        api_object_name = 'submission'
        model = Submission
        fields = (
            'id',
            'text',
            'author',
            'homework',
            'grade',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'author',
            'homework',
            'grade',
            'created_at',
            'updated_at',
        )


class HomeWorkSerializer(serializers.ModelSerializer):

    class Meta:
        api_object_name = 'homework'
        model = HomeWork
        fields = (
            'id',
            'text',
            'lecture',
            'author',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'lecture',
            'author',
            'created_at',
            'updated_at',
        )


class MyHomeWorkSerializer(serializers.ModelSerializer):

    submissions = SubmissionSerializer(many=True)

    class Meta:
        api_object_name = 'homework'
        model = HomeWork
        fields = (
            'id',
            'text',
            'lecture',
            'submissions',
            'author',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'lecture',
            'submissions',
            'author',
            'created_at',
            'updated_at',
        )
