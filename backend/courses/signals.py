from django.db.models.signals import post_save
from django.dispatch import receiver

from api.v1.notifications import NotificationSenderV1
from project.constants import EventEnum

from .models import Course


@receiver(post_save, sender=Course)
def course_post_save(sender, instance, created, **kwargs):
    event = EventEnum.CREATE if created else EventEnum.UPDATE
    sender = NotificationSenderV1(instance=instance, event=event)
    sender.send()
