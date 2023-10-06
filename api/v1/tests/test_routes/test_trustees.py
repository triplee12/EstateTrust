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
