from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords


class CustomUser(AbstractUser):

    class Role(models.TextChoices):

        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'

    role = models.CharField(max_length=50, choices=Role, verbose_name='Role')
    history = HistoricalRecords()

    def __str__(self):
        return self.username
