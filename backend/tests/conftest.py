import shutil
import tempfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APIClient

try:
    from courses.models import Course
except (NameError, ImportError) as e:
    raise AssertionError("Model `Course` is not found") from e

try:
    from courses.models import Lecture
except (NameError, ImportError) as e:
    raise AssertionError("Model `Lecture` is not found") from e

try:
    from courses.models import HomeWork
except (NameError, ImportError) as e:
    raise AssertionError("Model `HomeWork` is not found") from e

try:
    from courses.models import Submission
except (NameError, ImportError) as e:
    raise AssertionError("Model `Submission` is not found") from e

try:
    from courses.models import Grade
except (NameError, ImportError) as e:
    raise AssertionError("Model `Grade` is not found") from e

try:
    from courses.models import Comment
except (NameError, ImportError) as e:
    raise AssertionError("Model `Comment` is not found") from e


DATETIMEFORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
PASSWORD = "pass"
TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@pytest.fixture
def teacher(db, django_user_model):
    """Fixture `User` TEACHER."""
    return django_user_model.objects.create_user(
        username="teacher", email="p@p.fake2", password=PASSWORD, is_active=True, role="TEACHER"
    )


@pytest.fixture
def student(db, django_user_model):
    """Fixture `User` STUDENT."""
    return django_user_model.objects.create_user(
        username="student", email="p@p.fake2", password=PASSWORD, is_active=True, role="STUDENT"
    )


@pytest.fixture
def another_teacher(db, django_user_model):
    return django_user_model.objects.create_user(
        username="another_teacher",
        password="password123",  # NOQA: S106
        role="TEACHER",
    )


@pytest.fixture
def another_student(db, django_user_model):
    """Fixture `User` STUDENT."""
    return django_user_model.objects.create_user(
        username="student2", email="p@p.fake2", password=PASSWORD, is_active=True, role="STUDENT"
    )


@pytest.fixture
def auth_client(db, request, teacher, another_teacher, student, another_student):
    client = APIClient()
    user = {
        "teacher": teacher,
        "student": student,
        "another_teacher": another_teacher,
        "another_student": another_student,
    }[request.param]
    client.force_authenticate(user)
    return client


@pytest.fixture
def anon_client(db):
    """Fixture `APIClient` without authorization."""
    return APIClient()


@pytest.fixture
def course(db, teacher):
    """Fixture `User` Course."""
    return Course.objects.create(
        title="string",
        author=teacher,
    )


@pytest.fixture
def someone_else_course(db, django_user_model):
    new_teacher = django_user_model.objects.create_user(
        username="new_teacher", email="p@p.fake2", password=PASSWORD, is_active=True, role="TEACHER"
    )
    return Course.objects.create(
        title="string",
        author=new_teacher,
    )


@pytest.fixture
def temp_media_root():
    temp_dir = tempfile.mkdtemp()
    with override_settings(MEDIA_ROOT=temp_dir):
        yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def lecture_payload(temp_media_root, teacher):
    """Fixture for data when creating a lecture."""
    return {
        "topic": "Новая лекция",
        "teacher": teacher.id,
        "presentation_file": SimpleUploadedFile(
            "new_presentation.pdf", b"file_content_for_new_lecture", content_type="application/pdf"
        ),
    }


@pytest.fixture
def lecture(db, temp_media_root, course, teacher):
    return Lecture.objects.create(
        topic="Introduction to testing",
        course=course,
        teacher=teacher,
        presentation_file=SimpleUploadedFile("lecture.txt", b"lecture content"),
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
    return Submission.objects.create(text="dslfnlasndflksdanf", author=student, homework=homework)


@pytest.fixture
def another_submission(db, another_student, homework):
    return Submission.objects.create(text="lkmlkadsfml", author=another_student, homework=homework)


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
        text="comment",
        author=teacher,
        grade=grade,
    )
