from django.core.management.base import BaseCommand

from project.celery import debug_task


class Command(BaseCommand):
    help = "Fills the database with mock data."

    def handle(self, *args, **options):
        debug_task.delay()
