import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from courses.models import Submission

User = get_user_model()


@pytest.mark.parametrize('auth_client', ['teacher'], indirect=True)
def test_list_submissions_by_teacher(auth_client, homework, submission, another_submission):
    """Преподаватель курса может видеть все решения к домашнему заданию."""
    url = f'/api/v1/homeworks/{homework.id}/submissions/'
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2


@pytest.mark.parametrize('auth_client', ['student'], indirect=True)
def test_list_submissions_by_student_forbidden(auth_client, homework, submission, another_submission):
    """Студент может видеть только свои."""
    url = f'/api/v1/homeworks/{homework.id}/submissions/'
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['id'] == submission.id


def test_list_submissions_unauthenticated(anon_client, homework, submission, another_submission):
    """Анонимный пользователь не может видеть список решений."""
    url = f'/api/v1/homeworks/{homework.id}/submissions/'
    response = anon_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize('auth_client', ['student'], indirect=True)
def test_create_submission_by_student(auth_client, homework):
    """Студент, записанный на курс, может отправить решение."""
    url = f'/api/v1/homeworks/{homework.id}/submissions/'
    payload = {
        "text": "string",
    }
    response = auth_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert Submission.objects.filter(id=response.data['id'])


@pytest.mark.parametrize('auth_client', ['teacher'], indirect=True)
def test_create_submission_by_teacher_forbidden(auth_client, homework):
    """Преподаватель не может отправлять решение."""
    url = f'/api/v1/homeworks/{homework.id}/submissions/'
    payload = {
        "text": "string",
    }
    response = auth_client.post(url, payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize('auth_client', ['student'], indirect=True)
def test_retrieve_own_submission_by_student(auth_client, homework, submission):
    """Студент может просматривать свое решение."""
    url = f'/api/v1/homeworks/{homework.id}/submissions/{submission.id}/'
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == submission.id


@pytest.mark.parametrize('auth_client', ['student'], indirect=True)
def test_retrieve_others_submission_by_student_forbidden(auth_client, homework, another_submission):
    """Студент не может просматривать чужое решение."""
    url = f'/api/v1/homeworks/{homework.id}/submissions/{another_submission.id}/'
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize('auth_client', ['teacher'], indirect=True)
def test_retrieve_submission_by_teacher(auth_client, homework, submission, another_submission):
    """Преподаватель может просматривать любое решение в своем курсе."""
    for submission in (submission, another_submission):
        url = f'/api/v1/homeworks/{homework.id}/submissions/{submission.id}/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == submission.id


@pytest.mark.parametrize('auth_client', ['student'], indirect=True)
def test_update_own_submission_by_student(auth_client, homework, submission):
    """Студент может обновить свое решение."""
    url = f'/api/v1/homeworks/{homework.id}/submissions/{submission.id}/'
    payload = {
        "text": "updated",
    }
    response = auth_client.patch(url, payload)
    assert response.status_code == status.HTTP_200_OK
    submission.refresh_from_db()
    assert response.data['text'] == submission.text


@pytest.mark.parametrize('auth_client', ['student'], indirect=True)
def test_delete_own_submission_by_student(auth_client, homework, submission):
    """Студент может удалить свое решение."""
    url = f'/api/v1/homeworks/{homework.id}/submissions/{submission.id}/'
    payload = {
        "text": "updated",
    }
    response = auth_client.delete(url, payload)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Submission.objects.filter(id=submission.id).exists()
