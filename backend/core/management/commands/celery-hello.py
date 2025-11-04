from django.core.management.base import BaseCommand

from project.celery import debug_classed_task, debug_task, high_task, low_task, print_obj_task, undefined_task
from users.models import CustomUser


class Command(BaseCommand):
    help = "Fills the database with mock data."

    def handle(self, *args, **options):
        debug_task.apply_async()
        debug_classed_task.delay()
        low_task.delay()
        high_task.delay()
        undefined_task.delay()
        user = CustomUser.objects.first()
        if user:
            print_obj_task.delay(user)
            print(f'{user} sent in celery')
        else:
            print('User not found')
