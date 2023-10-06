#!/usr/bin/python3
"""Test assets routes for EstateTrust."""

from typing import Dict
import pytest
from jose import jwt
from api.v1.configurations.settings import settings
from api.v1.models.schemas.users import AccessToken


@pytest.mark.order(after="test_beneficiaries.py::test_delete_beneficiary")
def test_create_asset(client) -> Dict[str, str]:
    """Test adding an asset."""
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
    asset = client.post(
        f"/api/v1/assets/{user_id}/create/asset",
        headers=headers, json={
            "name": "Four storey building",
            "location": "21 housing Awada Onitsha, Anambra state Nigeria",
            "will_to": beneficiaries.json()[0]["uuid_pk"],
            "note": """
            I Ejie Emmanuel Chukwebuka will Three hundred thousand
            United State dollar ($300,000.00) to my first son MySon."""
        }
    )
    res_data = {
        "message": "asset added successfully"
    }
    assert asset.status_code == 201
    assert asset.json() == res_data


@pytest.mark.order(after="test_assets.py::test_create_asset")
def test_retrieve_assets(client):
    """Test retrieve_assets."""
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
    assets = client.get(
        f"/api/v1/assets/grantor/{user_id}/assets",
        headers=headers
    )
    assert assets.status_code == 200
    assert len(assets.json()) == 1


@pytest.mark.order(after="test_assets.py::test_retrieve_assets")
def test_retrieve_assets_for_beneficiary(client):
    """Test retrieve assets for a benefiticiary."""
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
    assets = client.get(
        f"/api/v1/assets/beneficiary/{beneficiaries.json()[0]['uuid_pk']}/assets",
        headers=headers
    )
    assert assets.status_code == 200
    assert len(assets.json()) == 1


@pytest.mark.order(
    after="test_assets.py::test_retrieve_assets_for_beneficiary"
)
def test_retrieve_asset(client):
    """Test retrieve an asset."""
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
    assets = client.get(
        f"/api/v1/assets/grantor/{user_id}/assets",
        headers=headers
    )
    asset = client.get(
        f"/api/v1/assets/{user_id}/assets/{assets.json()[0]['uuid_pk']}",
        headers=headers
    )
    assert asset.status_code == 200


@pytest.mark.order(after="test_assets.py::test_retrieve_asset")
def test_update_asset(client):
    """Update an asset."""
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
    assets = client.get(
        f"/api/v1/assets/grantor/{user_id}/assets",
        headers=headers
    )
    asset = client.put(
        f"/api/v1/assets/{user_id}/assets/{assets.json()[0]['uuid_pk']}/update",
        headers=headers, json={
            "name": "Updated four storey building"
        }
    )
    assert asset.status_code == 200


@pytest.mark.order(after="test_assets.py::test_update_asset")
def test_delete_asset(client):
    """Delete an asset."""
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
    assets = client.get(
        f"/api/v1/assets/grantor/{user_id}/assets",
        headers=headers
    )
    asset = client.delete(
        f"/api/v1/assets/{user_id}/assets/{assets.json()[0]['uuid_pk']}/delete",
        headers=headers
    )
    assert asset.status_code == 204
