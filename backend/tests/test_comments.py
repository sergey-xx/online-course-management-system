from courses.models import Comment
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


def test_create_comment_by_student_or_teacher(auth_client_teacher, auth_client_student, grade):
    url = f'/api/v1/submissions/grade/{grade.pk}/comments/'
    payload = {
        'text': 'test_text'
    }
    for client in (auth_client_teacher, auth_client_student):
        response = client.post(url, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == payload['text']


def test_create_comment_by_another_student(auth_client_another_student, grade):
    url = f'/api/v1/submissions/grade/{grade.pk}/comments/'
    payload = {
        'text': 'test_text'
    }
    response = auth_client_another_student.post(url, payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_retrieve_comment(
        auth_client_teacher,
        auth_client_student,
        auth_client_another_teacher,
        comment,
):
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    for client in (auth_client_teacher, auth_client_student, auth_client_another_teacher):
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == comment.text


def test_retrieve_comment_anoter_student(
        auth_client_another_student,
        comment,
):
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    response = auth_client_another_student.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_comment_by_author(
    auth_client_teacher,
    comment,
):
    payload = {'text': 'new comment'}
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    response = auth_client_teacher.patch(url, payload)
    assert response.status_code == status.HTTP_200_OK
    comment.refresh_from_db()
    assert comment.text == payload['text']


def test_update_comment_by_non_author(
    auth_client_student,
    auth_client_another_teacher,
    auth_client_another_student,
    comment,
):
    payload = {'text': 'new comment'}
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    for client in (auth_client_student, auth_client_another_student, auth_client_another_teacher):
        response = client.patch(url, payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_comment_by_author(auth_client_teacher, comment,):
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    response = auth_client_teacher.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.filter(id=comment.id).exists()


def test_delete_comment_by_non_author(
    auth_client_student,
    auth_client_another_teacher,
    auth_client_another_student,
    comment,
):
    url = f'/api/v1/submissions/grade/{comment.grade.pk}/comments/{comment.pk}/'
    for client in (auth_client_student, auth_client_another_student, auth_client_another_teacher):
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        comment.refresh_from_db()
