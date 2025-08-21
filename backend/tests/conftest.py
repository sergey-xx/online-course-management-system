import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

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

try:
    from courses.models import HomeWork
except (NameError, ImportError):
    raise AssertionError(
        'Model `HomeWork` is not found'
    )

try:
    from courses.models import Submission
except (NameError, ImportError):
    raise AssertionError(
        'Model `Submission` is not found'
    )

try:
    from courses.models import Grade
except (NameError, ImportError):
    raise AssertionError(
        'Model `Grade` is not found'
    )

try:
    from courses.models import Comment
except (NameError, ImportError):
    raise AssertionError(
        'Model `Comment` is not found'
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
    """Fixture `User` STUDENT."""
    return django_user_model.objects.create_user(
        username='student',
        email='p@p.fake2',
        password=PASSWORD,
        is_active=True,
        role='STUDENT'
    )


@pytest.fixture()
def another_student(db, django_user_model):
    """Fixture `User` STUDENT."""
    return django_user_model.objects.create_user(
        username='student2',
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
def auth_client_another_student(db, another_student):
    """Fixture `APIClient` with authorizated user."""
    client = APIClient()
    client.force_authenticate(another_student)
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


@pytest.fixture
def another_teacher(db, django_user_model):
    return django_user_model.objects.create_user(
        username='another_teacher',
        password='password123',
        role='TEACHER'
    )


@pytest.fixture
def auth_client_another_teacher(db, another_teacher):
    client = APIClient()
    client.force_authenticate(another_teacher)
    return client


@pytest.fixture
def lecture_payload(teacher):
    """Фикстура для данных при создании лекции."""
    return {
        "topic": "Новая лекция",
        "teacher": teacher.id,
        "presentation_file": SimpleUploadedFile(
            "new_presentation.pdf",
            b"file_content_for_new_lecture",
            content_type="application/pdf"
        ),
    }


@pytest.fixture
def lecture(db, course, teacher):
    return Lecture.objects.create(
        topic="Введение в тестирование",
        course=course,
        teacher=teacher,
        presentation_file=SimpleUploadedFile("lecture.txt", b"lecture content")
    )


@pytest.fixture
def homework(db, teacher, lecture):
    return HomeWork.objects.create(
        text="dslfnlasndflksdanf",
        lecture=lecture,
        author=teacher,
    )


@pytest.fixture
def submission(db, student, homework):
    return Submission.objects.create(
        text="dslfnlasndflksdanf",
        author=student,
        homework=homework
    )


@pytest.fixture
def another_submission(db, another_student, homework):
    return Submission.objects.create(
        text="dslfnlasndflksdanf",
        author=another_student,
        homework=homework
    )


@pytest.fixture
def grade(db, submission, teacher):
    return Grade.objects.create(
        submission=submission,
        score=1,
        author=teacher,
    )


@pytest.fixture
def comment(db, grade, teacher):
    return Comment.objects.create(
        text='comment',
        author=teacher,
        grade=grade,
    )
