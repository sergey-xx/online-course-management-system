from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.exceptions import Conflict
from django.db.utils import IntegrityError

from .models import Comment, Course, HomeWork, Lecture, Submission, Grade

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
            'teachers': {'required': False, 'allow_empty': True},
            'students': {'required': False, 'allow_empty': True},
        }


class LectureSerializers(serializers.ModelSerializer):

    class Meta:
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


class GradeSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(source='submission_id', read_only=True)

    class Meta:
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

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except IntegrityError:
            raise Conflict(f'Submission {kwargs["submission"].pk} already has Grade')


class SubmissionSerializers(serializers.ModelSerializer):

    grade = GradeSerializers(read_only=True)

    class Meta:
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
            'grade,'
            'created_at',
            'updated_at',
        )


class HomeWorkSerializers(serializers.ModelSerializer):

    class Meta:
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


class MyHomeWorkSerializers(serializers.ModelSerializer):

    submissions = SubmissionSerializers(many=True)

    class Meta:
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
