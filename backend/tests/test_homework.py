import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from courses.models import HomeWork

User = get_user_model()

PAYLOAD = {'text': 'text'}


def test_list_homeworks_unauthenticated(anon_client, lecture):
    url = f'/api/v1/lectures/{lecture.id}/homeworks/'
    response = anon_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize('auth_client', ['teacher', 'student'], indirect=True)
def test_list_homeworks_authenticated(auth_client, homework):
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/'
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['text'] == homework.text


@pytest.mark.parametrize('auth_client', ['teacher'], indirect=True)
def test_create_homework_by_lecture_author(auth_client, lecture):
    url = f'/api/v1/lectures/{lecture.id}/homeworks/'
    start_count = HomeWork.objects.count()
    response = auth_client.post(url, PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    assert HomeWork.objects.count() == start_count + 1
    HomeWork.objects.get(id=response.data['id'])


@pytest.mark.parametrize('auth_client', ['another_teacher'], indirect=True)
def test_create_homework_by_other_teacher_forbidden(auth_client, lecture):
    url = f'/api/v1/lectures/{lecture.id}/homeworks/'
    start_count = HomeWork.objects.count()
    response = auth_client.post(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert HomeWork.objects.count() == start_count


@pytest.mark.parametrize('auth_client', ['student'], indirect=True)
def test_create_homework_by_student_forbidden(auth_client, lecture):
    url = f'/api/v1/lectures/{lecture.id}/homeworks/'
    start_count = HomeWork.objects.count()
    response = auth_client.post(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert HomeWork.objects.count() == start_count


@pytest.mark.parametrize('auth_client', ['teacher', 'student', 'another_teacher'], indirect=True)
def test_retrieve_homework(auth_client, homework):
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['text'] == homework.text


@pytest.mark.parametrize('auth_client', ['teacher'], indirect=True)
def test_update_homework_by_author(auth_client, homework):
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    start_count = HomeWork.objects.count()
    response = auth_client.patch(url, PAYLOAD)
    assert response.status_code == status.HTTP_200_OK
    assert HomeWork.objects.count() == start_count
    new = HomeWork.objects.get(id=response.data['id'])
    assert new.text == PAYLOAD['text']


@pytest.mark.parametrize('auth_client', ['another_teacher'], indirect=True)
def test_update_homework_by_other_teacher_forbidden(auth_client, homework):
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client.patch(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize('auth_client', ['student'], indirect=True)
def test_update_homework_by_student_forbidden(auth_client, homework):
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client.patch(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize('auth_client', ['teacher',], indirect=True)
def test_delete_homework_by_author(auth_client, lecture, teacher):
    homework = HomeWork.objects.create(
        text='To Delete',
        lecture=lecture,
        author=teacher
    )
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not HomeWork.objects.filter(id=homework.id).exists()


@pytest.mark.parametrize('auth_client', ['another_teacher'], indirect=True)
def test_delete_homework_by_other_teacher_forbidden(auth_client, lecture, teacher):
    homework = HomeWork.objects.create(
        text='To Delete',
        lecture=lecture,
        author=teacher
    )
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert HomeWork.objects.filter(id=homework.id).exists()


@pytest.mark.parametrize('auth_client', ['student'], indirect=True)
def test_delete_homework_by_student_forbidden(auth_client, lecture, teacher):
    homework = HomeWork.objects.create(
        text='To Delete',
        lecture=lecture,
        author=teacher
    )
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert HomeWork.objects.filter(id=homework.id).exists()
