from django.contrib.auth import get_user_model
from rest_framework import status

from courses.models import HomeWork

User = get_user_model()

PAYLOAD = {'text': 'text'}


def test_list_homeworks_unauthenticated(anon_client, lecture):
    url = f'/api/v1/lectures/{lecture.id}/homeworks/'
    response = anon_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_homeworks_authenticated(auth_client_teacher, auth_client_student, homework):
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/'
    for auth_client in (auth_client_teacher, auth_client_student):
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['text'] == homework.text


def test_create_homework_by_lecture_author(auth_client_teacher, lecture):
    url = f'/api/v1/lectures/{lecture.id}/homeworks/'
    start_count = HomeWork.objects.count()
    response = auth_client_teacher.post(url, PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    assert HomeWork.objects.count() == start_count + 1
    HomeWork.objects.get(id=response.data['id'])


def test_create_homework_by_other_teacher_forbidden(auth_client_another_teacher, lecture):
    url = f'/api/v1/lectures/{lecture.id}/homeworks/'
    start_count = HomeWork.objects.count()
    response = auth_client_another_teacher.post(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert HomeWork.objects.count() == start_count


def test_create_homework_by_student_forbidden(auth_client_student, lecture):
    url = f'/api/v1/lectures/{lecture.id}/homeworks/'
    start_count = HomeWork.objects.count()
    response = auth_client_student.post(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert HomeWork.objects.count() == start_count


def test_retrieve_homework(auth_client_student, auth_client_teacher, auth_client_another_teacher, homework):
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    for auth_client in (auth_client_teacher, auth_client_student, auth_client_another_teacher):
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == homework.text


def test_update_homework_by_author(auth_client_teacher, homework):
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    start_count = HomeWork.objects.count()
    response = auth_client_teacher.patch(url, PAYLOAD)
    assert response.status_code == status.HTTP_200_OK
    assert HomeWork.objects.count() == start_count
    new = HomeWork.objects.get(id=response.data['id'])
    assert new.text == PAYLOAD['text']


def test_update_homework_by_other_teacher_forbidden(auth_client_another_teacher, homework):
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client_another_teacher.patch(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_homework_by_student_forbidden(auth_client_student, homework):
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client_student.patch(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_homework_by_author(auth_client_teacher, lecture, teacher):
    homework = HomeWork.objects.create(
        text='To Delete',
        lecture=lecture,
        author=teacher
    )
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client_teacher.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not HomeWork.objects.filter(id=homework.id).exists()


def test_delete_homework_by_other_teacher_forbidden(auth_client_another_teacher, lecture, teacher):
    homework = HomeWork.objects.create(
        text='To Delete',
        lecture=lecture,
        author=teacher
    )
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client_another_teacher.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert HomeWork.objects.filter(id=homework.id).exists()


def test_delete_homework_by_student_forbidden(auth_client_student, lecture, teacher):
    homework = HomeWork.objects.create(
        text='To Delete',
        lecture=lecture,
        author=teacher
    )
    url = f'/api/v1/lectures/{homework.lecture_id}/homeworks/{homework.id}/'
    response = auth_client_student.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert HomeWork.objects.filter(id=homework.id).exists()
