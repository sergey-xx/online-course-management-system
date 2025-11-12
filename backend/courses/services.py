from django.db import transaction
from django.db.utils import IntegrityError

from core.exceptions import Conflict
from core.services import AuthorService
from courses.models import Comment, Course, Grade, HomeWork, Lecture, Submission


class CourseService(AuthorService):
    """A service class to handle business logic related to courses."""

    @transaction.atomic
    def create(self, **kwargs):
        teachers = kwargs.pop("teachers", None)
        students = kwargs.pop("students", None)
        course = Course.objects.create(author=self.author, **kwargs)
        if teachers:
            course.teachers.set(teachers)
        if students:
            course.students.set(students)
        return course

    @transaction.atomic
    def update(self, instance, **kwargs):
        teachers = kwargs.pop("teachers", None)
        students = kwargs.pop("students", None)
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        if teachers:
            instance.teachers.set(teachers)
        if students:
            instance.students.set(students)
        instance.save()
        return instance


class LectureService(AuthorService):
    """A service class to handle business logic related to lectures."""

    model = Lecture

    def create(self, *args, **kwargs):
        return self.model.objects.create(*args, **kwargs)


class HomeWorkService(AuthorService):
    """A service class to handle business logic related to homeworks."""

    model = HomeWork


class SubmissionService(AuthorService):
    """A service class to handle business logic related to submissions."""

    model = Submission


class GradingService(AuthorService):
    """A service class to handle business logic related to gradings."""

    model = Grade

    def create(self, **kwargs) -> Grade:
        try:
            return super().create(**kwargs)
        except IntegrityError as e:
            submission = kwargs.get("submission")
            raise Conflict(f"Submission {submission.pk} already has a Grade.") from e


class CommentService(AuthorService):
    """A service class to handle business logic related to comments."""

    model = Comment
