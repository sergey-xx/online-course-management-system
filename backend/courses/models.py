from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):

    title = models.CharField(max_length=255, verbose_name='Title')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'}, verbose_name='Author'
    )
    teachers = models.ManyToManyField(
        User, related_name='teacher_courses', limit_choices_to={'role': 'TEACHER'}, verbose_name='Teachers'
    )
    students = models.ManyToManyField(
        User, related_name='student_courses', limit_choices_to={'role': 'STUDENT'}, verbose_name='Students'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation datetime')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updation datetime')

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.id}:{self.title}'


class Lecture(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures', verbose_name='Course')
    topic = models.CharField(max_length=255, verbose_name='Topic')
    presentation_file = models.FileField(blank=True, null=True, verbose_name='Presentation file')
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='Schedulled date and time')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation datetime')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updation datetime')

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.id}:{self.topic}'


class HomeWork(models.Model):

    text = models.TextField(verbose_name='Text')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='homeworks', verbose_name='Lecture')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation datetime')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updation datetime')

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.id}:{self.text[:20]}'


class Submission(models.Model):

    text = models.TextField(verbose_name='Text')
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'},
        related_name='student_submissions', verbose_name='Student'
    )
    homework = models.ForeignKey(
        HomeWork, on_delete=models.CASCADE, related_name='submissions', verbose_name='HomeWork'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation datetime')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updation datetime')

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.id} Student:{self.student_id} HW:{self.homework_id}'


class Grade(models.Model):

    score = models.PositiveSmallIntegerField(verbose_name='Score')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'},
        related_name='teacher_grades', verbose_name='Author'
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'},
        related_name='student_grades', verbose_name='Student'
    )
    homework = models.ForeignKey(HomeWork, on_delete=models.CASCADE, related_name='grades', verbose_name='HomeWork')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation datetime')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updation datetime')

    class Meta:
        unique_together = ('student', 'homework')

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.id} Grade:{self.grade_id} Author:{self.author_id}'


class Comment(models.Model):

    text = models.TextField(verbose_name='Text')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='comments', verbose_name='Grade')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation datetime')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updation datetime')

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.id} Grade:{self.grade_id} Author:{self.author_id}'
