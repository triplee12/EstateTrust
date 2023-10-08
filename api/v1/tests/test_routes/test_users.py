#!/usr/bin/python3
"""Test users routes."""

from typing import Dict
from jose import jwt
from api.v1.configurations.settings import settings
from api.v1.models.schemas.users import AccessToken


def test_create_grantor_account(client) -> Dict[str, str]:
    """Test create grantor account."""
    grantor = client.post(
        "/api/v1/grantors/account/create",
        json={
            "first_name": "ChukwuEbuka",
            "last_name": "Ejie",
            "middle_name": "Emmanuel",
            "username": "eBolton",
            "password": "07067Oliver",
            "email": "tripleeoliver3@gmail.com",
            "phone_number": "+2348153836254",
            "date_of_birth": "2000-07-18",
            "gender": "male"
        }
    )
    res_data = {
        "status_code": 201,
        "message": "Account created successfully"
    }
    assert grantor.json() == res_data
    assert grantor.status_code == 201


def test_create_grantor_account_fail(client) -> Dict[str, str]:
    """Test create grantor account fail."""
    grantor = client.post(
        "/api/v1/grantors/account/create",
        json={
            "first_name": "ChukwuEbuka",
            "last_name": "Ejie",
            "middle_name": "Emmanuel",
            "username": "eBolton",
            "password": "07067Oliver",
            "email": "tripleeoliver3@gmail.com",
            "phone_number": "+2348153836254",
            "date_of_birth": "2000-07-18",
            "gender": "male"
        }
    )
    res_data = {
        "detail": "Error creating account."
    }
    assert grantor.json() == res_data
    assert grantor.status_code == 422


def test_user_dashboard(client) -> Dict[str, str]:
    """Test that user dashboard is accessible."""
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
    grantor = client.get(
        f"/api/v1/grantors/account/dashboard/{user_id}",
        headers=headers
    )
    assert grantor.status_code == 200
    assert grantor.json()["uuid_pk"] == user_id


def test_update_account(client):
    """Test update_account."""
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
    grantor = client.put(
        f"/api/v1/grantors/account/dashboard/{user_id}/update",
        headers=headers,
        json={
            "first_name": "Tester",
            "last_name": "Ejie",
            "middle_name": "Yours",
            "username": "eBolton",
            "password": "07067Oliver",
            "email": "tripleeoliver3@gmail.com",
            "phone_number": "+2348153836254",
            "date_of_birth": "2000-07-18",
            "gender": "male"
        }
    )
    assert grantor.status_code == 200
    assert grantor.json()["first_name"] == "Tester"
    assert grantor.json()["middle_name"] == "Yours"


def test_update_account_fail(client):
    """Test update_account failure."""
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
    grantor = client.put(
        f"/api/v1/grantors/account/dashboard/{user_id}/update",
        headers=headers,
        json={
            "username": "aBolton"
        }
    )
    assert grantor.status_code == 422


def test_delete_account(client):
    """Test delete account."""
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
    grantor = client.delete(
        f"/api/v1/grantors/account/dashboard/{user_id}/delete",
        headers=headers
    )
    assert grantor.status_code == 204
