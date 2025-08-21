import pytest
from rest_framework.test import APIClient

try:
    from courses.models import Course
except (NameError, ImportError):
    raise AssertionError(
        'Model `Course` is not found'
    )

try:
    from courses.models import Lecture
except (NameError, ImportError):
    raise AssertionError(
        'Model `Lecture` is not found'
    )


DATETIMEFORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
PASSWORD = 'pass'


@pytest.fixture()
def teacher(db, django_user_model):
    """Fixture `User` TEACHER."""
    return django_user_model.objects.create_user(
        username='teacher',
        email='p@p.fake2',
        password=PASSWORD,
        is_active=True,
        role='TEACHER'
    )


@pytest.fixture()
def student(db, django_user_model):
    """Fixture `User` TEACHER."""
    return django_user_model.objects.create_user(
        username='student',
        email='p@p.fake2',
        password=PASSWORD,
        is_active=True,
        role='STUDENT'
    )


@pytest.fixture()
def auth_client_teacher(db, teacher):
    """Fixture `APIClient` with authorizated user."""
    client = APIClient()
    client.force_authenticate(teacher)
    return client


@pytest.fixture()
def auth_client_student(db, student):
    """Fixture `APIClient` with authorizated user."""
    client = APIClient()
    client.force_authenticate(student)
    return client


@pytest.fixture()
def anon_client(db):
    """Fixture `APIClient` without authorization."""
    client = APIClient()
    return client


@pytest.fixture()
def course(db, teacher):
    """Fixture `User` Course."""
    return Course.objects.create(
        title='string',
        author=teacher,
    )


@pytest.fixture()
def someone_else_course(db, django_user_model):
    new_teacher = django_user_model.objects.create_user(
        username='new_teacher',
        email='p@p.fake2',
        password=PASSWORD,
        is_active=True,
        role='TEACHER'
    )
    return Course.objects.create(
        title='string',
        author=new_teacher,
    )
