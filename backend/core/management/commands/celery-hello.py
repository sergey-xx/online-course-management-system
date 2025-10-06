from django.core.management.base import BaseCommand

from project.celery import debug_classed_task, debug_task


class Command(BaseCommand):
    help = "Fills the database with mock data."

    def handle(self, *args, **options):
        debug_task.apply_async()
        debug_classed_task.delay()
