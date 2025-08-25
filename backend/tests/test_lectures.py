import pytest

from courses.models import Lecture

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('auth_client', ['teacher', 'student', 'another_teacher', 'another_student'], indirect=True)
def test_list_lectures_by_anyone(auth_client, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/'
    response = auth_client.get(url)
    assert response.status_code == 200, f"Ошибка для клиента: {auth_client}"
    data = response.json()
    assert 'results' in data
    assert len(data['results']) == 1
    assert data['results'][0]['id'] == lecture.id


@pytest.mark.parametrize('auth_client', ['teacher', 'student', 'another_teacher', 'another_student'], indirect=True)
def test_retrieve_lecture_by_anyone(auth_client, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
    response = auth_client.get(url)
    assert response.status_code == 200, f"Ошибка для клиента: {auth_client}"
    data = response.json()
    assert data['id'] == lecture.id
    assert data['topic'] == lecture.topic


@pytest.mark.parametrize('auth_client', ['teacher'], indirect=True)
def test_create_lecture_by_course_teacher_success(auth_client, course, lecture_payload):
    url = f'/api/v1/courses/{course.id}/lectures/'
    response = auth_client.post(url, data=lecture_payload, format='multipart')
    assert response.status_code == 201
    data = response.json()
    assert data['topic'] == lecture_payload['topic']
    assert Lecture.objects.filter(id=data['id']).exists()


@pytest.mark.parametrize('auth_client', ['student', 'another_student',], indirect=True)
def test_create_lecture_by_student_forbidden(auth_client, course, lecture_payload):
    url = f'/api/v1/courses/{course.id}/lectures/'
    response = auth_client.post(url, data=lecture_payload, format='multipart')
    assert response.status_code == 403


@pytest.mark.parametrize('auth_client', ['another_teacher',], indirect=True)
def test_create_lecture_by_another_teacher_forbidden(auth_client, course, lecture_payload):
    url = f'/api/v1/courses/{course.id}/lectures/'
    response = auth_client.post(url, data=lecture_payload, format='multipart')
    assert response.status_code == 403


@pytest.mark.parametrize('auth_client', ['teacher',], indirect=True)
def test_update_lecture_by_course_teacher_success(auth_client, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
    payload = {"topic": "Обновленный заголовок лекции"}
    response = auth_client.patch(url, data=payload, format='multipart')
    assert response.status_code == 200
    lecture.refresh_from_db()
    assert lecture.topic == payload['topic']


@pytest.mark.parametrize('auth_client', ['student',], indirect=True)
def test_update_lecture_by_student_forbidden(auth_client, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
    payload = {"topic": "Обновлено студентом"}
    response = auth_client.patch(url, data=payload, format='multipart')
    assert response.status_code == 403


@pytest.mark.parametrize('auth_client', ['teacher',], indirect=True)
def test_delete_lecture_by_course_teacher_success(auth_client, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert not Lecture.objects.filter(id=lecture.id).exists()


@pytest.mark.parametrize('auth_client', ['student',], indirect=True)
def test_delete_lecture_by_student_forbidden(auth_client, course, lecture):
    url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
    response = auth_client.delete(url)
    assert response.status_code == 403
    assert Lecture.objects.filter(id=lecture.id).exists()
