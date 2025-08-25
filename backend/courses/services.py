from typing import Iterable

from django.db import transaction
from django.db.utils import IntegrityError

from core.exceptions import Conflict
from core.services import AuthorService
from courses.models import Comment, Course, Grade, HomeWork, Lecture, Submission


class CourseService(AuthorService):

    @transaction.atomic
    def create(self, title, teachers: Iterable, students: Iterable):
        course = Course.objects.create(title=title, author=self.author,)
        if teachers:
            course.teachers.set(teachers)
        if students:
            course.students.set(students)
        return course


class LectureService(AuthorService):

    def create(self, *args, **kwargs):
        return Lecture.objects.create(
            *args, **kwargs
        )


class HomeWorkService(AuthorService):

    def create(self, *args, **kwargs):
        return HomeWork.objects.create(
            author=self.author,
            *args, **kwargs
        )


class SubmissionService(AuthorService):

    def create(self, *args, **kwargs):
        return Submission.objects.create(
            author=self.author,
            *args, **kwargs
        )


class GradingService(AuthorService):
    """
    A service class to handle business logic related to grading.
    """

    def create(self, submission: Submission, score: int) -> Grade:
        try:
            grade = Grade.objects.create(
                submission=submission,
                score=score,
                author=self.author
            )
            return grade
        except IntegrityError:
            raise Conflict(f'Submission {submission.pk} already has a Grade.')


class CommentService(AuthorService):
    """
    A service class to handle business logic related to Comments.
    """

    def create(self, *args, **kwargs):
        return Comment.objects.create(
            author=self.author,
            *args, **kwargs
        )
