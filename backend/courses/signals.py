from django.db.models.signals import post_save
from django.dispatch import receiver

from project.constants import ChannelGroup, EventEnum
from project.notifications import send_object_to_group

from .models import Course


@receiver(post_save, sender=Course)
def course_post_save(sender, instance, created, **kwargs):
    event = EventEnum.CREATE if created else EventEnum.UPDATE
    send_object_to_group(ChannelGroup.NOTIFICATION, event, instance)
