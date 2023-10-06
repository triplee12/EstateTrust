#!/usr/bin/python3
"""Test beneficiaries routes for EstateTrust."""

from typing import Dict
import pytest
from jose import jwt
from api.v1.configurations.settings import settings
from api.v1.models.schemas.users import AccessToken


@pytest.mark.order(after="test_users.py::test_create_grantor_account")
def test_login(client) -> Dict[str, str]:
    """Test login function."""
    data = client.post(
        "/api/v1/auths/account/login",
        json={
            "username": "eBolton",
            "password": "07067Oliver",
            'account_type': 'grantor'
        }
    )
    assert data.status_code == 200
    assert isinstance(data.json(), dict)
    assert data.json()["token_type"] == "bearer"


@pytest.mark.order(after="test_authenticate.py::test_login")
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
        "/api/v1/auths/account/login",
        json={
            "username": username,
            "password": password,
            'account_type': 'grantor'
        }
    )
    assert data.status_code == status_code
    assert isinstance(data.json(), dict)


@pytest.mark.order(after="test_authenticate.py::test_login_fail")
def test_user_access_token(client):
    """Test access token for validation"""
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
    username: str = decoded_jwt.get("username")

    assert isinstance(user_id, str)
    assert username == "eBolton"
    assert login_data.token_type == "bearer"
