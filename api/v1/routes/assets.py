#!/usr/bin/python3
"""Assets router for Estate Trust."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from api.v1.authorizations.oauth import get_current_user
from api.v1.configurations.database import get_db
from api.v1.models.data.users import User
from api.v1.models.schemas.assets import AddAsset, AssetRes, UpdateAsset
from api.v1.repositories.assets import AssetRepository

asset_router = APIRouter(
    prefix="/assets",
    tags=["assets", "Asset"]
)


@asset_router.post(
    "/{grantor_id}/create/asset",
    status_code=status.HTTP_201_CREATED
)
async def create_asset(
    grantor_id: str, data: AddAsset,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Add asset to database."""
    repo = AssetRepository(sess)
    if current_user.uuid_pk == grantor_id:
        grantor = sess.query(User).filter(User.uuid_pk == grantor_id).first()
        data.owner_id = grantor.uuid_pk
        added = repo.add_asset(data=data)
        if added:
            return {
                "message": "asset added successfully"
            }
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="error occurred while adding asset"
        )


@asset_router.get(
    "/grantor/{grantor_id}/assets",
    response_model=List[AssetRes]
)
async def retrieve_assets(
    grantor_id: str, current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Retrieve all assets for a specific grantor."""
    repo = AssetRepository(sess)
    if current_user.uuid_pk == grantor_id:
        assets = repo.get_all_assests_for_grantor(user_id=grantor_id)
        if assets is None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="no assets found"
            )
        return assets


@asset_router.get(
    "/beneficiary/{bene_id}/assets", response_model=List[AssetRes]
)
async def retrieve_assets_for_beneficiary(
    bene_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Retrieve all assets for a specific beneficiary."""
    repo = AssetRepository(sess)
    if current_user:
        assets = repo.get_all_assests_for_beneficiary(user_id=bene_id)
        if assets is None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="no assets found"
            )
        return assets


@asset_router.get("/{grantor_id}/assets/{asset_id}", response_model=AssetRes)
async def retrieve_asset(
    grantor_id: str, asset_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Retrieve an asset."""
    repo = AssetRepository(sess)
    if current_user:
        asset = repo.get_asset(user_id=grantor_id, asset_id=asset_id)
        if asset:
            return asset
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="asset not found"
        )


@asset_router.patch(
    "/{grantor_id}/assets/{asset_id}/update",
    response_model=AssetRes
)
async def update_asset(
    grantor_id: str, asset_id: str, data: UpdateAsset,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Update an asset."""
    repo = AssetRepository(sess)
    if current_user:
        asset = repo.update_asset(
            user_id=grantor_id, asset_id=asset_id, data=data
        )
        if asset:
            return asset
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="error occurred while updating asset data"
        )


@asset_router.delete(
    "/{grantor_id}/assets/{asset_id}/delete"
)
async def delete_asset(
    grantor_id: str, asset_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Delete an asset."""
    repo = AssetRepository(sess)
    if current_user:
        asset = repo.delete_asset(
            user_id=grantor_id, asset_id=asset_id
        )
        if asset:
            return
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="error occurred while deleting asset"
        )
