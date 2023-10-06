#!/usr/bin/python3
"""Test trustees routes for EstateTrust."""

from typing import Dict
import pytest
from jose import jwt
from api.v1.configurations.settings import settings
from api.v1.models.schemas.users import AccessToken


@pytest.mark.order(after="test_users.py::test_create_grantor_account")
@pytest.mark.parametrize(
    "first_name, middle_name, last_name, phone_number, email, username, password, relation, note, status_code",
    [
        (
            "Trustee", "Trustee", "Mytrustee",
            "+12345678900", "mytrustee@gmail.com",
            "trustee", "password", "lawyer",
            "I Ejie Emmanuel Chukwuebuka",
            201
        ),
        (
            "Trustee1", "Trustee1", "Mytrustee1",
            "+12345678901", "mytrustee1@gmail.com",
            "trustee1", "password", "lawyer",
            "I Ejie Emmanuel Chukwuebuka",
            201
        ),
        (
            "Trustee2", "Trustee2", "Mytrustee2",
            "+12345678902", "mytrustee@gmail.com",
            "trustee2", "password", "brother",
            "I Ejie Emmanuel Chukwuebuka",
            201
        )
    ]
)
def test_create_trustee(
    client, first_name,
    middle_name, last_name,
    phone_number, email,
    username, password,
    relation, note, status_code
) -> Dict[str, str]:
    """Test create trustee account."""
    SECRET_KEY = settings.OAUTH2_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    res = client.post('/api/v1/auths/account/login', json={
        'username': 'eBolton',
        'password': '07067Oliver',
        'account_type': 'grantor'
    })
    login_data = AccessToken(**res.json())
    decoded_jwt = jwt.decode(
        login_data.access_token,
        SECRET_KEY, algorithms=[ALGORITHM]
    )
    user_id = decoded_jwt.get("uuid_pk")
    headers = {
        'Authorization': 'Bearer {}'.format(login_data.access_token)
    }
    trustee = client.post(
        f"/api/v1/trustees/account/{user_id}/create/trustees",
        headers=headers, json={
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "phone_number": phone_number,
            "email": email,
            "username": username,
            "password": password,
            "relation": relation,
            "note": note
        }
    )
    res_data = {
        "message": "Trustee added successfully"
    }
    assert trustee.status_code == status_code
    assert trustee.json() == res_data


@pytest.mark.order(after="test_trustees.py::test_create_trustee")
def test_retrieve_trustees(client):
    """Test retrieve_trustees."""
    SECRET_KEY = settings.OAUTH2_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    res = client.post('/api/v1/auths/account/login', json={
        'username': 'eBolton',
        'password': '07067Oliver',
        'account_type': 'grantor'
    })
    login_data = AccessToken(**res.json())
    decoded_jwt = jwt.decode(
        login_data.access_token,
        SECRET_KEY, algorithms=[ALGORITHM]
    )
    user_id = decoded_jwt.get("uuid_pk")
    headers = {
        'Authorization': 'Bearer {}'.format(login_data.access_token)
    }
    trustees = client.get(
        f"/api/v1/trustees/account/{user_id}/trustees",
        headers=headers
    )
    assert trustees.status_code == 200
    assert len(trustees.json()) == 3


@pytest.mark.order(after="test_trustees.py::test_retrieve_trustees")
def test_retrieve_trustee(client):
    """Test retrieve_trustee."""
    SECRET_KEY = settings.OAUTH2_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    res = client.post('/api/v1/auths/account/login', json={
        'username': 'eBolton',
        'password': '07067Oliver',
        'account_type': 'grantor'
    })
    login_data = AccessToken(**res.json())
    decoded_jwt = jwt.decode(
        login_data.access_token,
        SECRET_KEY, algorithms=[ALGORITHM]
    )
    user_id = decoded_jwt.get("uuid_pk")
    headers = {
        'Authorization': 'Bearer {}'.format(login_data.access_token)
    }
    trustees = client.get(
        f"/api/v1/trustees/account/{user_id}/trustees",
        headers=headers
    )
    trustee_id = trustees.json()[0]["uuid_pk"]
    trustee = client.get(
        f"/api/v1/trustees/account/{user_id}/trustees/{trustee_id}",
        headers=headers
    )

    assert trustee.status_code == 200
    assert trustee.json()["added_by"] == user_id


@pytest.mark.order(after="test_trustees.py::test_retrieve_trustee")
def test_update_trustee_account(client):
    """Test update_trustee_account."""
    SECRET_KEY = settings.OAUTH2_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    res = client.post('/api/v1/auths/account/login', json={
        'username': 'eBolton',
        'password': '07067Oliver',
        'account_type': 'grantor'
    })
    login_data = AccessToken(**res.json())
    decoded_jwt = jwt.decode(
        login_data.access_token,
        SECRET_KEY, algorithms=[ALGORITHM]
    )
    user_id = decoded_jwt.get("uuid_pk")
    headers = {
        'Authorization': 'Bearer {}'.format(login_data.access_token)
    }
    trustees = client.get(
        f"/api/v1/trustees/account/{user_id}/trustees",
        headers=headers
    )
    trustee_id = trustees.json()[0]["uuid_pk"]
    trustee = client.put(
        f"/api/v1/trustees/account/{user_id}/trustees/{trustee_id}/update",
        headers=headers, json={
            "first_name": "John",
            "last_name": "Bob"
        }
    )
    assert trustee.status_code == 200
    assert trustee.json()["first_name"] == "John"
    assert trustee.json()["last_name"] == "Bob"


@pytest.mark.order(after="test_trustees.py::test_update_trustee_account")
def test_delete_trustee(client):
    """Test delete trustee account."""
    SECRET_KEY = settings.OAUTH2_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    res = client.post('/api/v1/auths/account/login', json={
        'username': 'eBolton',
        'password': '07067Oliver',
        'account_type': 'grantor'
    })
    login_data = AccessToken(**res.json())
    decoded_jwt = jwt.decode(
        login_data.access_token,
        SECRET_KEY, algorithms=[ALGORITHM]
    )
    user_id = decoded_jwt.get("uuid_pk")
    headers = {
        'Authorization': 'Bearer {}'.format(login_data.access_token)
    }
    trustees = client.get(
        f"/api/v1/trustees/account/{user_id}/trustees",
        headers=headers
    )
    trustee_id = trustees.json()[0]["uuid_pk"]
    trustee = client.delete(
        f"/api/v1/trustees/account/{user_id}/trustees/{trustee_id}/delete",
        headers=headers
    )
    assert trustee.status_code == 204
