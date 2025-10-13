from django.contrib.auth import get_user_model
from django.db import models
from simple_history.models import HistoricalRecords

from core.models import DatedModel

User = get_user_model()


class Course(DatedModel):

    title = models.CharField(max_length=255, verbose_name='Title')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'}, verbose_name='Author'
    )
    teachers = models.ManyToManyField(
        User, blank=True, related_name='teacher_courses', limit_choices_to={'role': 'TEACHER'}, verbose_name='Teachers'
    )
    students = models.ManyToManyField(
        User, blank=True, related_name='student_courses', limit_choices_to={'role': 'STUDENT'}, verbose_name='Students'
    )
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.id}:{self.title}'

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ('id',)


class Lecture(DatedModel):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures', verbose_name='Course')
    topic = models.CharField(max_length=255, verbose_name='Topic')
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'}, verbose_name='Teacher'
    )
    presentation_file = models.FileField(blank=True, null=True, verbose_name='Presentation file')
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='Schedulled date and time')
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.id}:{self.topic}'

    class Meta:
        verbose_name = 'Lecture'
        verbose_name_plural = 'Lectures'
        ordering = ('id',)


class HomeWork(DatedModel):

    text = models.TextField(verbose_name='Text')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='homeworks', verbose_name='Lecture')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'}, verbose_name='Author'
    )
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.id}:{self.text[:20]}'

    class Meta:
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'
        ordering = ('id',)


class Submission(DatedModel):

    text = models.TextField(verbose_name='Text')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'},
        related_name='submissions', verbose_name='Author'
    )
    homework = models.ForeignKey(
        HomeWork, on_delete=models.CASCADE, related_name='submissions', verbose_name='HomeWork'
    )
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.id} Student:{self.author_id} HW:{self.homework_id}'

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
        ordering = ('id',)


class Grade(DatedModel):

    submission = models.OneToOneField(
        Submission, on_delete=models.CASCADE, primary_key=True, verbose_name='Submission'
    )
    score = models.PositiveSmallIntegerField(verbose_name='Score')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'},
        related_name='teacher_grades', verbose_name='Author'
    )
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.submission_id} Score: {self.score} Author:{self.author_id}'

    class Meta:
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
        ordering = ('submission_id',)


class Comment(DatedModel):

    text = models.TextField(verbose_name='Text')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='comments', verbose_name='Grade')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Author')
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.id} Grade:{self.grade_id} Author:{self.author_id}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('id',)
