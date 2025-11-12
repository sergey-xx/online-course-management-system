from django.core.management.base import BaseCommand

from courses.models import Course
from project.constants import ChannelGroup
from project.notifications import send_object_to_group


class Command(BaseCommand):
    help = "Testing command."

    def handle(self, *args, **options):
        # del options
        course = Course.objects.first()
        send_object_to_group(ChannelGroup.NOTIFICATION, course)


def handle(*args, **kwargs):
    course = Course.objects.first()
    send_object_to_group(ChannelGroup.NOTIFICATION, course)
