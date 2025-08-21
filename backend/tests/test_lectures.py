import pytest

from courses.models import Lecture

pytestmark = pytest.mark.django_db


def test_list_lectures_by_anyone(auth_client_student, auth_client_teacher, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/'
    clients = [auth_client_student, auth_client_teacher]
    for client in clients:
        response = client.get(url)
        assert response.status_code == 200, f"Ошибка для клиента: {client}"
        data = response.json()
        assert 'results' in data
        assert len(data['results']) == 1
        assert data['results'][0]['id'] == lecture.id


def test_retrieve_lecture_by_anyone(auth_client_student, auth_client_teacher, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
    clients = [auth_client_student, auth_client_teacher]
    for client in clients:
        response = client.get(url)
        assert response.status_code == 200, f"Ошибка для клиента: {client}"
        data = response.json()
        assert data['id'] == lecture.id
        assert data['topic'] == lecture.topic


def test_create_lecture_by_course_teacher_success(auth_client_teacher, course, lecture_payload):
    url = f'/api/v1/courses/{course.id}/lectures/'
    response = auth_client_teacher.post(url, data=lecture_payload, format='multipart')
    assert response.status_code == 201
    data = response.json()
    assert data['topic'] == lecture_payload['topic']
    assert Lecture.objects.filter(id=data['id']).exists()


def test_create_lecture_by_student_forbidden(auth_client_student, course, lecture_payload):
    url = f'/api/v1/courses/{course.id}/lectures/'
    response = auth_client_student.post(url, data=lecture_payload, format='multipart')
    assert response.status_code == 403


def test_create_lecture_by_another_teacher_forbidden(auth_client_another_teacher, course, lecture_payload):
    url = f'/api/v1/courses/{course.id}/lectures/'
    response = auth_client_another_teacher.post(url, data=lecture_payload, format='multipart')
    assert response.status_code == 403


def test_update_lecture_by_course_teacher_success(auth_client_teacher, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
    payload = {"topic": "Обновленный заголовок лекции"}
    response = auth_client_teacher.patch(url, data=payload, format='multipart')
    assert response.status_code == 200
    lecture.refresh_from_db()
    assert lecture.topic == payload['topic']


def test_update_lecture_by_student_forbidden(auth_client_student, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
    payload = {"topic": "Обновлено студентом"}
    response = auth_client_student.patch(url, data=payload, format='multipart')
    assert response.status_code == 403


def test_delete_lecture_by_course_teacher_success(auth_client_teacher, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
    response = auth_client_teacher.delete(url)
    assert response.status_code == 204
    assert not Lecture.objects.filter(id=lecture.id).exists()


def test_delete_lecture_by_student_forbidden(auth_client_student, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
    response = auth_client_student.delete(url)
    assert response.status_code == 403
    assert Lecture.objects.filter(id=lecture.id).exists()
