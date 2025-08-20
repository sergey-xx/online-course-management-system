from django.contrib.auth import get_user_model
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist

import pytest


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'field', [
        'email',
        'first_name',
        'last_name',
        'username',
        'role'])
def test_user_model_has_expected_fields(field):
    User = get_user_model()
    try:
        User._meta.get_field(field)
    except FieldDoesNotExist:
        assert False, (
            f'Make sure that the `User` model has the `{field}` field.'
        )


@pytest.mark.parametrize(
    'role', ['TEACHER', 'STUDENT']
)
def test_registration(anon_client, role):
    url = '/api/v1/auth/users/'
    payload = {
        "email": "user@example.com",
        "username": "string",
        "password": "VUnTDBAVmFYKeRP3XRo",
        "role": role
    }
    response = anon_client.post(url, data=payload, format='json')
    assert response.status_code == 201
    data = response.json()
    assert data['role'] == role


@pytest.mark.parametrize(
    'role', ['BLABLA', 'HUMAN', 'ADMIN', '', None]
)
def test_registration_with_uncorrect_role(anon_client, role):
    url = '/api/v1/auth/users/'
    payload = {
        "email": "user@example.com",
        "username": "string",
        "password": "VUnTDBAVmFYKeRP3XRo",
        "role": role
    }
    response = anon_client.post(url, data=payload, format='json')
    assert response.status_code == 400
