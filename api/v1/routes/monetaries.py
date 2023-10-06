#!/usr/bin/python3
"""Monetaries router for Estate Trust."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from api.v1.authorizations.oauth import get_current_user
from api.v1.configurations.database import get_db
from api.v1.models.data.users import User
from api.v1.models.schemas.assets import (
    AddMonetary, MonetaryRes, UpdateMonetary
)
from api.v1.repositories.monetaries import MonetaryRepository
from api.v1.utils.documents import download_file, upload_file

monetary_router = APIRouter(
    prefix="/monetaries",
    tags=["monetaries", "Monetary"]
)


@monetary_router.post(
    "/asset/{grantor_id}/create/monetary",
    status_code=status.HTTP_201_CREATED
)
async def create_monetary_asset(
    grantor_id: str, data: AddMonetary,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Add a new monetary asset.

    Method: POST
    Args:
        data (dict): dictionary containing monetary asset's data
    Returns:
        return 201 if successful, 422 otherwise
    """
    repo = MonetaryRepository(sess)
    if current_user.uuid_pk == grantor_id:
        grantor = sess.query(User).filter(User.uuid_pk == grantor_id).first()
        data.owner_id = grantor.uuid_pk
        up_file = await upload_file(data.document)
        data.document = up_file["filename"]
        added = repo.add_monetary_asset(data=data)
        if added:
            return {
                "message": "monetary asset added successfully"
            }
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="error occurred while adding asset"
        )


@monetary_router.get("/asset/download/{file_name}")
async def download_file_route(
    file_name: str, grantor_id: str,
    current_user: str = Depends(get_current_user)
):
    """Download file route."""
    if current_user.uuid_pk == grantor_id:
        file = await download_file(file_name)
        return file


@monetary_router.get(
    "/asset/asset/{grantor_id}/assets",
    response_model=List[MonetaryRes]
)
async def retrieve_monetary_assets(
    grantor_id: str, current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Retrieve all assets for a specific grantor.

    Method: GET
    Args:
        grantor_id (str): ID of the grantor
    Returns:
        list of monentary assets information
    """
    repo = MonetaryRepository(sess)
    if current_user.uuid_pk == grantor_id:
        assets = repo.get_all_monetary_assets_for_grantor(
            grantor_id=grantor_id
        )
        if assets is None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="no assets found"
            )
        return assets


@monetary_router.get(
    "/asset/beneficiary/{bene_id}/assets", response_model=List[MonetaryRes]
)
async def retrieve_monetary_assets_for_beneficiary(
    bene_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Retrieve all assets for a specific beneficiary.

    Method: GET
    Args:
        bene_id (str): ID of the beneficiary
    Returns:
        list of monentary assets information
    """
    repo = MonetaryRepository(sess)
    if current_user:
        assets = repo.get_all_monetary_assets_for_beneficiary(will_to=bene_id)
        if assets is None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="no assets found"
            )
        return assets


@monetary_router.get(
    "/asset/grantor/{grantor_id}/assets/{asset_id}",
    response_model=MonetaryRes
)
async def retrieve_monetary_asset(
    grantor_id: str, asset_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Retrieve a monetary asset.

    Method: GET
    Args:
        grantor_id (str): ID of the grantor
        asset_id (str): ID of the asset to retrieve
    Returns:
        dictionary of asset's information
    """
    repo = MonetaryRepository(sess)
    if current_user:
        asset = repo.get_asset(grantor_id=grantor_id, asset_id=asset_id)
        if asset:
            return asset
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="asset not found"
        )


@monetary_router.put(
    "/asset/grantor/{grantor_id}/assets/{asset_id}/update",
    response_model=MonetaryRes
)
async def update_asset(
    grantor_id: str, asset_id: str, data: UpdateMonetary,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Update an asset.

    Method: PATCH
    Args:
        grantor_id (str): ID of the grantor
        asset_id (str): ID of the asset to be updated
        data: dictionary containing asset's data to be updated
    Returns:
        dictionary of asset's information
    """
    repo = MonetaryRepository(sess)
    if current_user:
        if data.document:
            up_file = await upload_file(data.document)
            data.document = up_file["filename"]
        asset = repo.update_asset(
            grantor_id=grantor_id, asset_id=asset_id, data=data
        )
        if asset:
            return asset
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="error occurred while updating asset data"
        )


@monetary_router.delete(
    "/asset/grantor/{grantor_id}/assets/{asset_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_asset(
    grantor_id: str, asset_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Delete an asset.

    Method: DELETE
    Args:
        grantor_id (str): ID of the grantor
        asset_id (str): ID of the monetary asset
    Returns:
        return 204 on success, 304 on failure
    """
    repo = MonetaryRepository(sess)
    if current_user:
        asset = repo.delete_asset(
            grantor_id=grantor_id, asset_id=asset_id
        )
        if asset:
            return
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="error occurred while deleting asset"
        )
