from rest_framework import status


def test_grade_submission_by_teacher(auth_client_teacher, submission):
    """Преподаватель курса может оценить решение."""
    url = f'/api/v1/submissions/{submission.id}/grade/'
    payload = {
        "score": 222
    }
    response = auth_client_teacher.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['score'] == payload['score']
    assert submission.grade.score == payload['score']


def test_grade_submission_by_student_forbidden(auth_client_student, submission):
    """Студент не может оценить решение."""
    url = f'/api/v1/submissions/{submission.id}/grade/'
    payload = {
        "score": 222
    }
    response = auth_client_student.post(url, payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN
