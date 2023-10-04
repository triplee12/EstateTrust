#!/usr/bin/python3
"""Test users routes."""

from typing import Dict, List
import pytest
from jose import jwt
from api.v1.configurations.settings import settings
from api.v1.models.schemas.users import AccessToken


def test_create_grantor_account(client) -> Dict[str, str]:
    """Test create grantor account."""
    grantor = client.post(
        "/grantors/account/create",
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
        "/grantors/account/create",
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


def test_login(client) -> Dict[str, str]:
    """Test login function."""
    data = client.post(
        "grantors/account/login",
        json={
            "username": "eBolton",
            "password": "07067Oliver"
        }
    )
    assert data.status_code == 200
    assert isinstance(data.json(), dict)
    assert data.json()["token_type"] == "bearer"


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("triplee1", "mYpassword", 401),
        ("passwordCantNotBeBlank", "000password", 401),
        ("triplee", None, 422),
        (None, "testpassword", 422),
        (None, None, 422),
        ("", None, 422),
        ("", "", 401),
        (11111, 22231, 422),
        (12.32, 1312.00, 422)
    ]
)
def test_login_fail(client, username, password, status_code):
    """Test login failure."""
    data = client.post(
        "grantors/account/login",
        json={
            "username": username,
            "password": password
        }
    )
    assert data.status_code == status_code
    assert isinstance(data.json(), dict)


def test_user_access_token(client):
    """Test access token for validation"""
    SECRET_KEY = settings.OAUTH2_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    res = client.post('/grantors/account/login', json={
        'username': 'eBolton',
        'password': '07067Oliver'
    })
    login_data = AccessToken(**res.json())
    decoded_jwt = jwt.decode(
        login_data.access_token,
        SECRET_KEY, algorithms=[ALGORITHM]
    )
    user_id = decoded_jwt.get("uuid_pk")
    username: str = decoded_jwt.get("username")

    assert isinstance(user_id, str)
    assert username == "eBolton"
    assert login_data.token_type == "bearer"


def test_user_dashboard(client) -> Dict[str, str]:
    """Test that user dashboard is accessible."""
    SECRET_KEY = settings.OAUTH2_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    res = client.post('/grantors/account/login', json={
        'username': 'eBolton',
        'password': '07067Oliver'
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
        f"/grantors/account/dashboard/{user_id}",
        headers=headers
    )
    assert grantor.status_code == 200
    assert grantor.json()["uuid_pk"] == user_id


def test_update_account(client):
    """Test update_account."""
    SECRET_KEY = settings.OAUTH2_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    res = client.post('/grantors/account/login', json={
        'username': 'eBolton',
        'password': '07067Oliver'
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
        f"/grantors/account/dashboard/{user_id}/update",
        headers=headers,
        json={
            "first_name": "Tester",
            "middle_name": "Yours"
        }
    )
    assert grantor.status_code == 200
    assert grantor.json()["first_name"] == "Tester"
    assert grantor.json()["middle_name"] == "Yours"


def test_update_account_fail(client):
    """Test update_account failure."""
    SECRET_KEY = settings.OAUTH2_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    res = client.post('/grantors/account/login', json={
        'username': 'eBolton',
        'password': '07067Oliver'
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
        f"/grantors/account/dashboard/{user_id}/update",
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

    res = client.post('/grantors/account/login', json={
        'username': 'eBolton',
        'password': '07067Oliver'
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
        f"/grantors/account/dashboard/{user_id}/delete",
        headers=headers
    )
    assert grantor.status_code == 204
