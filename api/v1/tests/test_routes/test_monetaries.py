#!/usr/bin/python3
"""Test monetary assets routes for EstateTrust."""

from typing import Dict
import pytest
from jose import jwt
from api.v1.configurations.settings import settings
from api.v1.models.schemas.users import AccessToken


@pytest.mark.order(after="test_assets.py::test_delete_asset")
def test_create_monetary_asset(client) -> Dict[str, str]:
    """Test creating a monetary asset."""
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
    monetary = client.post(
        f"/api/v1/monetaries/asset/{user_id}/create/monetary",
        headers=headers, json={
            "acc_name": "Okoye Chris Ebuka",
            "acc_number": "2070000000",
            "amount": "$300,000.00",
            "bank_name": "United Bank For Africa (UBA)",
            "will_to": beneficiaries.json()[0]["uuid_pk"],
            "note": """
            I Ejie Emmanuel Chukwebuka will Three hundred thousand
            United State dollar ($300,000.00) to my first son MySon.
            """
        }
    )
    assert monetary.status_code == 201
    assert monetary.json() == {
        "message": "monetary asset added successfully"
    }


@pytest.mark.order(
    after="test_monetaries.py::test_create_monetary_asset"
)
def test_retrieve_monetary_assets(client):
    """Test retrieve_monetary_assets."""
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
        f"/api/v1/monetaries/asset/grantor/{user_id}/assets",
        headers=headers
    )
    assert assets.status_code == 200
    assert len(assets.json()) == 1


@pytest.mark.order(after="test_monetaries.py::test_retrieve_monetary_assets")
def test_retrieve_monetary_assets_for_beneficiary(client):
    """Test retrieve monetary assets for a benefiticiary."""
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
    bene_id = beneficiaries.json()[0]['uuid_pk']
    assets = client.get(
        f"/api/v1/monetaries/asset/beneficiary/{bene_id}/assets",
        headers=headers
    )
    assert assets.status_code == 200
    assert len(assets.json()) == 1


@pytest.mark.order(
    after="test_monetaries.py::test_retrieve_monetary_assets_for_beneficiary"
)
def test_retrieve_monetary_asset(client):
    """Test retrieve a monetary asset."""
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
        f"/api/v1/monetaries/asset/grantor/{user_id}/assets",
        headers=headers
    )
    asset_id = assets.json()[0]['uuid_pk']
    asset = client.get(
        f"/api/v1/monetaries/asset/grantor/{user_id}/assets/{asset_id}",
        headers=headers
    )
    assert asset.status_code == 200


@pytest.mark.order(
    after="test_monetaries.py::test_retrieve_monetary_asset"
)
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
        f"/api/v1/monetaries/asset/grantor/{user_id}/assets",
        headers=headers
    )
    asset_id = assets.json()[0]['uuid_pk']
    asset = client.put(
        f"/api/v1/monetaries/asset/grantor/{user_id}/assets/{asset_id}/update",
        headers=headers, json={
            "acc_name": "Okoye Chris Edu"
        }
    )
    assert asset.status_code == 200


@pytest.mark.order(after="test_monetaries.py::test_update_asset")
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
        f"/api/v1/monetaries/asset/grantor/{user_id}/assets",
        headers=headers
    )
    asset_id = assets.json()[0]['uuid_pk']
    asset = client.delete(
        f"/api/v1/monetaries/asset/grantor/{user_id}/assets/{asset_id}/delete",
        headers=headers
    )
    assert asset.status_code == 204
