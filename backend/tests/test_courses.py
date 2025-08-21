import pytest
from django.core.exceptions import ObjectDoesNotExist


def test_course_creation(teacher, student, auth_client_teacher):
    url = '/api/v1/courses/'
    payload = {"title": "string", "teachers": [teacher.id], "students": [student.id]}
    response = auth_client_teacher.post(url, data=payload, format='json')
    assert response.status_code == 201
    data = response.json()
    for key in payload.keys():
        assert data[key] == payload[key]
    assert isinstance(data['id'], int) is True


def test_student_cant_create_couse(teacher, student, auth_client_student):
    url = '/api/v1/courses/'
    payload = {"title": "string", "teachers": [teacher.id], "students": [student.id]}
    response = auth_client_student.post(url, data=payload, format='json')
    assert response.status_code == 403


def test_course_update(teacher, student, course, auth_client_teacher):
    url = f'/api/v1/courses/{course.id}/'
    payload = {"title": f"{course.title}2", "teachers": [teacher.id], "students": [student.id]}
    response = auth_client_teacher.patch(url, data=payload, format='json')
    assert response.status_code == 200
    data = response.json()
    for key in payload.keys():
        assert data[key] == payload[key]
    assert isinstance(data['id'], int) is True


def test_student_cant_update_couse(teacher, student, course, auth_client_student):
    url = f'/api/v1/courses/{course.id}/'
    payload = {"title": f"{course.title}2", "teachers": [teacher.id], "students": [student.id]}
    response = auth_client_student.patch(url, data=payload, format='json')
    assert response.status_code == 403


def test_course_delete(course, auth_client_teacher):
    url = f'/api/v1/courses/{course.id}/'
    response = auth_client_teacher.delete(url)
    assert response.status_code == 204
    with pytest.raises(ObjectDoesNotExist):
        course.refresh_from_db()


def test_student_cant_delete_couse(course, auth_client_student):
    url = f'/api/v1/courses/{course.id}/'
    response = auth_client_student.delete(url)
    assert response.status_code == 403
    course.refresh_from_db()


def test_not_author_cant_change_course(teacher, student, someone_else_course, auth_client_teacher):
    url = f'/api/v1/courses/{someone_else_course.id}/'
    payload = {"title": f"{someone_else_course.title}2", "teachers": [teacher.id], "students": [student.id]}
    response = auth_client_teacher.patch(url, data=payload, format='json')
    assert response.status_code == 403
    response = auth_client_teacher.delete(url)
    assert response.status_code == 403
