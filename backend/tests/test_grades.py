from rest_framework import status

PAYLOAD = {"score": 222}


def test_create_grade_submission_by_teacher(auth_client_teacher, submission):
    url = f'/api/v1/submissions/{submission.id}/grade/'

    response = auth_client_teacher.post(url, PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['score'] == PAYLOAD['score']
    assert submission.grade.score == PAYLOAD['score']


def test_create_grade_submission_by_student_forbidden(auth_client_student, submission):
    url = f'/api/v1/submissions/{submission.id}/grade/'
    response = auth_client_student.post(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_grade_submission_by_teacher(auth_client_teacher, grade):
    url = f'/api/v1/submissions/{grade.submission_id}/grade/'
    response = auth_client_teacher.patch(url, PAYLOAD)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['score'] == PAYLOAD['score']
    grade.refresh_from_db()
    assert grade.score == PAYLOAD['score']


def test_update_grade_submission_by_student_forbidden(auth_client_student, grade):
    url = f'/api/v1/submissions/{grade.submission_id}/grade/'
    response = auth_client_student.patch(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN
