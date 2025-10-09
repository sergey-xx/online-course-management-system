import os
import time

import celery
from celery import Celery
from celery.schedules import crontab
from kombu.utils.json import register_type
from django.db.models import Model
from django.apps import apps


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


class ModelSerializer:

    @staticmethod
    def serialize(obj: Model):
        return [obj._meta.label, obj.pk]

    @staticmethod
    def deserialize(obj):
        return apps.get_model(obj[0]).objects.get(pk=obj[1])


register_type(
    Model,
    'model',
    ModelSerializer.serialize,
    ModelSerializer.deserialize
)


@app.task
def debug_task():
    """Test func."""
    time.sleep(5)
    print('Hello from debug task')


@app.task
def test(arg):
    print(arg)


@app.task
def add(x, y):
    z = x + y
    print(z)


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


class MyTask(celery.Task):

    def run(self, *args, **kwargs):
        print(f'Hello from {self.__class__.__name__}!')


class PrintObjectTask(celery.Task):

    def run(self, *args, **kwargs):
        print(f'Get {args} {kwargs}')


debug_classed_task = app.register_task(MyTask)
print_obj_task = app.register_task(PrintObjectTask)
