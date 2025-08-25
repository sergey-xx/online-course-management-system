import pytest
from rest_framework import status

PAYLOAD = {"score": 222}


@pytest.mark.parametrize('auth_client', ['teacher',], indirect=True)
def test_create_grade_submission_by_teacher(auth_client, submission):
    url = f'/api/v1/submissions/{submission.id}/grade/'
    response = auth_client.post(url, PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['score'] == PAYLOAD['score']
    assert submission.grade.score == PAYLOAD['score']


@pytest.mark.parametrize('auth_client', ['student',], indirect=True)
def test_create_grade_submission_by_student_forbidden(auth_client, submission):
    url = f'/api/v1/submissions/{submission.id}/grade/'
    response = auth_client.post(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize('auth_client', ['teacher',], indirect=True)
def test_update_grade_submission_by_teacher(auth_client, grade):
    url = f'/api/v1/submissions/{grade.submission_id}/grade/'
    response = auth_client.patch(url, PAYLOAD)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['score'] == PAYLOAD['score']
    grade.refresh_from_db()
    assert grade.score == PAYLOAD['score']


@pytest.mark.parametrize('auth_client', ['student',], indirect=True)
def test_update_grade_submission_by_student_forbidden(auth_client, grade):
    url = f'/api/v1/submissions/{grade.submission_id}/grade/'
    response = auth_client.patch(url, PAYLOAD)
    assert response.status_code == status.HTTP_403_FORBIDDEN
