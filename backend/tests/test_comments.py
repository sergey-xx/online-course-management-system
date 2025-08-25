import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from courses.models import Comment

User = get_user_model()


@pytest.mark.parametrize('auth_client', ['teacher', 'student'], indirect=True)
def test_create_comment_by_student_or_teacher(auth_client, grade):
    url = f'/api/v1/submissions/grade/{grade.pk}/comments/'
    payload = {
        'text': 'test_text'
    }
    response = auth_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['text'] == payload['text']


@pytest.mark.parametrize('auth_client', ['another_student'], indirect=True)
def test_create_comment_by_another_student(auth_client, grade):
    url = f'/api/v1/submissions/grade/{grade.pk}/comments/'
    payload = {
        'text': 'test_text'
    }
    response = auth_client.post(url, payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize('auth_client', ['teacher', 'another_teacher', 'student'], indirect=True)
def test_retrieve_comment(
        auth_client,
        comment,
):
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['text'] == comment.text


@pytest.mark.parametrize('auth_client', ['another_student',], indirect=True)
def test_retrieve_comment_anoter_student(
        auth_client,
        comment,
):
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize('auth_client', ['teacher',], indirect=True)
def test_update_comment_by_author(
    auth_client,
    comment,
):
    payload = {'text': 'new comment'}
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    response = auth_client.patch(url, payload)
    assert response.status_code == status.HTTP_200_OK
    comment.refresh_from_db()
    assert comment.text == payload['text']


@pytest.mark.parametrize('auth_client', ['another_student', 'another_teacher', 'student'], indirect=True)
def test_update_comment_by_non_author(
    auth_client,
    comment,
):
    payload = {'text': 'new comment'}
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    response = auth_client.patch(url, payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize('auth_client', ['teacher',], indirect=True)
def test_delete_comment_by_author(auth_client, comment,):
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.filter(id=comment.id).exists()


@pytest.mark.parametrize('auth_client', ['student', 'another_student', 'another_teacher'], indirect=True)
def test_delete_comment_by_non_author(auth_client, comment):
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    comment.refresh_from_db()
