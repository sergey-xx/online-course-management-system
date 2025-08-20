import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from courses.models import Lecture

# Помечаем все тесты в этом модуле для работы с БД
pytestmark = pytest.mark.django_db


@pytest.fixture
def another_teacher(db, django_user_model):
    """Фикстура для другого пользователя с ролью TEACHER."""
    return django_user_model.objects.create_user(
        username='another_teacher',
        password='password123',
        role='TEACHER'
    )


@pytest.fixture
def auth_client_another_teacher(db, another_teacher):
    """Фикстура для APIClient, аутентифицированного как another_teacher."""
    client = APIClient()
    client.force_authenticate(another_teacher)
    return client


@pytest.fixture
def lecture(db, course, teacher):
    """Фикстура для экземпляра лекции."""
    return Lecture.objects.create(
        topic="Введение в тестирование",
        course=course,
        teacher=teacher,
        presentation_file=SimpleUploadedFile("lecture.txt", b"lecture content")
    )


@pytest.fixture
def lecture_payload(teacher):
    """Фикстура для данных при создании лекции."""
    return {
        "topic": "Новая лекция",
        "teacher": teacher.id,
        "presentation_file": SimpleUploadedFile(
            "new_presentation.pdf",
            b"file_content_for_new_lecture",
            content_type="application/pdf"
        ),
    }


class TestLectureViewSet:
    """Тесты для LectureViewSet."""

    # --- Тесты на получение списка (List) ---

    def test_list_lectures_by_anyone(self, auth_client_student, auth_client_teacher, course, lecture):
        """
        Тест: любой пользователь (студент, преподаватель) может просматривать список лекций.
        """
        url = f'/api/v1/courses/{course.id}/lectures/'
        clients = [auth_client_student, auth_client_teacher]
        for client in clients:
            response = client.get(url)
            assert response.status_code == 200, f"Ошибка для клиента: {client}"
            data = response.json()
            assert 'results' in data
            assert len(data['results']) == 1
            assert data['results'][0]['id'] == lecture.id

    def test_retrieve_lecture_by_anyone(self, auth_client_student, auth_client_teacher, course, lecture):
        """
        Тест: любой пользователь может получить конкретную лекцию.
        """
        url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
        clients = [auth_client_student, auth_client_teacher]
        for client in clients:
            response = client.get(url)
            assert response.status_code == 200, f"Ошибка для клиента: {client}"
            data = response.json()
            assert data['id'] == lecture.id
            assert data['topic'] == lecture.topic

    def test_create_lecture_by_course_teacher_success(self, auth_client_teacher, course, lecture_payload):
        """
        Тест: преподаватель курса может создать лекцию.
        """
        url = f'/api/v1/courses/{course.id}/lectures/'
        response = auth_client_teacher.post(url, data=lecture_payload, format='multipart')
        assert response.status_code == 201
        data = response.json()
        assert data['topic'] == lecture_payload['topic']
        assert Lecture.objects.filter(id=data['id']).exists()

    def test_create_lecture_by_student_forbidden(self, auth_client_student, course, lecture_payload):
        """
        Тест: студент не может создать лекцию.
        """
        url = f'/api/v1/courses/{course.id}/lectures/'
        response = auth_client_student.post(url, data=lecture_payload, format='multipart')
        assert response.status_code == 403

    def test_create_lecture_by_another_teacher_forbidden(self, auth_client_another_teacher, course, lecture_payload):
        """
        Тест: преподаватель, не связанный с курсом, не может создать лекцию.
        """
        url = f'/api/v1/courses/{course.id}/lectures/'
        response = auth_client_another_teacher.post(url, data=lecture_payload, format='multipart')
        assert response.status_code == 403

    # --- Тесты на обновление (Update) ---

    def test_update_lecture_by_course_teacher_success(self, auth_client_teacher, course, lecture):
        """
        Тест: преподаватель курса может обновить лекцию.
        """
        url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
        payload = {"topic": "Обновленный заголовок лекции"}
        response = auth_client_teacher.patch(url, data=payload, format='multipart')
        assert response.status_code == 200
        lecture.refresh_from_db()
        assert lecture.topic == payload['topic']

    def test_update_lecture_by_student_forbidden(self, auth_client_student, course, lecture):
        """
        Тест: студент не может обновить лекцию.
        """
        url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
        payload = {"topic": "Обновлено студентом"}
        response = auth_client_student.patch(url, data=payload, format='multipart')
        assert response.status_code == 403

    # --- Тесты на удаление (Delete) ---

    def test_delete_lecture_by_course_teacher_success(self, auth_client_teacher, course, lecture):
        """
        Тест: преподаватель курса может удалить лекцию.
        """
        url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
        response = auth_client_teacher.delete(url)
        assert response.status_code == 204
        assert not Lecture.objects.filter(id=lecture.id).exists()

    def test_delete_lecture_by_student_forbidden(self, auth_client_student, course, lecture):
        """
        Тест: студент не может удалить лекцию.
        """
        url = f'/api/v1/courses/{course.id}/lectures/{lecture.id}/'
        response = auth_client_student.delete(url)
        assert response.status_code == 403
        assert Lecture.objects.filter(id=lecture.id).exists()
