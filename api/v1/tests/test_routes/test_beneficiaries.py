#!/usr/bin/python3
"""Test beneficiaries routes for EstateTrust."""

from typing import Dict
import pytest
from jose import jwt
from api.v1.configurations.settings import settings
from api.v1.models.schemas.users import AccessToken


@pytest.mark.order(after="test_trustees.py::test_delete_trustee")
@pytest.mark.parametrize(
    "first_name, middle_name, last_name, relation, status_code",
    [
        (
            "Chi", "Ben", "Ebuka",
            "son", 201
        ),
        (
            "Edu", "Chris", "Ebuka",
            "grandchild", 201
        ),
        (
            "Chiamaka", "Nedu", "Ebuka",
            "daughter", 201
        ),
        (
            "Ada", "Jenny", "Ebuka",
            "wife", 201
        )
    ]
)
def test_create_beneficiary(
    client, first_name,
    middle_name, last_name,
    relation, status_code
) -> Dict[str, str]:
    """Test create beneficiary account."""
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
    beneficiary = client.post(
        f"/api/v1/beneficiaries/account/{user_id}/create/beneficiary",
        headers=headers, json={
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "relation": relation
        }
    )
    res_data = {
        "message": "Beneficiary added successfully"
    }
    assert beneficiary.status_code == status_code
    assert beneficiary.json() == res_data


@pytest.mark.order(after="test_beneficiaries.py::test_create_beneficiary")
def test_retrieve_beneficiaries(client):
    """Test retrieve_beneficiaries."""
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
    beneficiaries = client.get(
        f"/api/v1/beneficiaries/account/{user_id}/beneficiaries",
        headers=headers
    )
    assert beneficiaries.status_code == 200
    assert len(beneficiaries.json()) == 4


@pytest.mark.order(after="test_beneficiaries.py::test_retrieve_beneficiaries")
def test_get_beneficiary(client):
    """Test get_beneficiary."""
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
    beneficiaries = client.get(
        f"/api/v1/beneficiaries/account/{user_id}/beneficiaries",
        headers=headers
    )
    bene_id = beneficiaries.json()[0]["uuid_pk"]
    beneficiary = client.get(
        f"/api/v1/beneficiaries/account/{user_id}/beneficiaries/{bene_id}",
        headers=headers
    )

    assert beneficiary.status_code == 200
    assert beneficiary.json()["added_by"] == user_id


@pytest.mark.order(after="test_beneficiaries.py::test_get_beneficiary")
def test_update_beneficiary(client):
    """Test update_beneficiary."""
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
    beneficiaries = client.get(
        f"/api/v1/beneficiaries/account/{user_id}/beneficiaries",
        headers=headers
    )
    bene_id = beneficiaries.json()[0]["uuid_pk"]
    beneficiary = client.put(
        f"/api/v1/beneficiaries/account/{user_id}/beneficiaries/{bene_id}/update",
        headers=headers, json={
            "first_name": "John",
            "middle_name": "Edu",
            "last_name": "Bob",
            "relation": "son"
        }
    )
    assert beneficiary.status_code == 200
    assert beneficiary.json()["first_name"] == "John"
    assert beneficiary.json()["last_name"] == "Bob"


@pytest.mark.order(after="test_beneficiaries.py::test_update_beneficiary")
def test_delete_beneficiary(client):
    """Test delete beneficiary account."""
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
    beneficiaries = client.get(
        f"/api/v1/beneficiaries/account/{user_id}/beneficiaries",
        headers=headers
    )
    bene_id = beneficiaries.json()[0]["uuid_pk"]
    beneficiary = client.delete(
        f"/api/v1/beneficiaries/account/{user_id}/beneficiaries/{bene_id}/delete",
        headers=headers
    )
    assert beneficiary.status_code == 204
