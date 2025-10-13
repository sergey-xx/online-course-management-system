from django.db import models


class DatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation datetime')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updation datetime')

    class Meta:
        abstract = True
