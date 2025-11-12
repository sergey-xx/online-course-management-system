import pytest
from django.core.exceptions import ObjectDoesNotExist


@pytest.mark.parametrize("auth_client", ["teacher"], indirect=True)
def test_course_creation(teacher, student, auth_client):
    url = "/api/v1/courses/"
    payload = {"title": "string", "teachers": [teacher.id], "students": [student.id]}
    response = auth_client.post(url, data=payload, format="json")
    assert response.status_code == 201
    data = response.json()
    for key in payload:
        assert data[key] == payload[key]
    assert isinstance(data["id"], int) is True


@pytest.mark.parametrize("auth_client", ["student"], indirect=True)
def test_student_cant_create_couse(teacher, student, auth_client):
    url = "/api/v1/courses/"
    payload = {"title": "string", "teachers": [teacher.id], "students": [student.id]}
    response = auth_client.post(url, data=payload, format="json")
    assert response.status_code == 403


@pytest.mark.parametrize("auth_client", ["teacher"], indirect=True)
def test_course_update(teacher, student, course, auth_client):
    url = f"/api/v1/courses/{course.id}/"
    payload = {"title": f"{course.title}2", "teachers": [teacher.id], "students": [student.id]}
    response = auth_client.patch(url, data=payload, format="json")
    assert response.status_code == 200
    data = response.json()
    for key in payload:
        assert data[key] == payload[key]
    assert isinstance(data["id"], int) is True


@pytest.mark.parametrize("auth_client", ["student"], indirect=True)
def test_student_cant_update_couse(teacher, student, course, auth_client):
    url = f"/api/v1/courses/{course.id}/"
    payload = {"title": f"{course.title}2", "teachers": [teacher.id], "students": [student.id]}
    response = auth_client.patch(url, data=payload, format="json")
    assert response.status_code == 403


@pytest.mark.parametrize("auth_client", ["teacher"], indirect=True)
def test_course_delete(course, auth_client):
    url = f"/api/v1/courses/{course.id}/"
    response = auth_client.delete(url)
    assert response.status_code == 204
    with pytest.raises(ObjectDoesNotExist):
        course.refresh_from_db()


@pytest.mark.parametrize("auth_client", ["student"], indirect=True)
def test_student_cant_delete_couse(course, auth_client):
    url = f"/api/v1/courses/{course.id}/"
    response = auth_client.delete(url)
    assert response.status_code == 403
    course.refresh_from_db()


@pytest.mark.parametrize("auth_client", ["teacher"], indirect=True)
def test_not_author_cant_change_course(teacher, student, someone_else_course, auth_client):
    url = f"/api/v1/courses/{someone_else_course.id}/"
    payload = {"title": f"{someone_else_course.title}2", "teachers": [teacher.id], "students": [student.id]}
    response = auth_client.patch(url, data=payload, format="json")
    assert response.status_code == 403
    response = auth_client.delete(url)
    assert response.status_code == 403
