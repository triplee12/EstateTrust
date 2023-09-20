#!/usr/bin/python3
"""Assets repository for Estate Trust."""

from typing import List
from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from api.v1.configurations.database import get_db
from api.v1.models.data.users import Beneficiary, User
from api.v1.models.data.assets import Asset


class AssetRepository:
    """Assets repository."""

    def __init__(self, sess: Session = Depends(get_db)) -> None:
        """Initialize the repository."""
        self.sess: Session = sess

    def add_asset(self, data) -> bool:
        """Add an asset."""
        asset = Asset(**data)
        self.sess.add(asset)
        self.sess.commit()
        if asset:
            return True
        return False

    def get_all_assests_for_grantor(self, user_id: UUID) -> List[Asset] | None:
        """
        Retrieve all assets for a given user.

        Args:
            user_id (UUID): The grantor's unique ID
        Returns:
            The list of assests if user exists, or None otherwise
        """
        try:
            user = self.sess.query(User).filter(
                User.uuid_pk == user_id
            ).first()
            if user:
                assets = user.assets
                return assets
            return None
        except DataError:
            return None

    def get_all_assests_for_beneficiary(
        self, user_id: UUID
    ) -> List[Asset] | None:
        """
        Retrieve all assets for a given beneficiary.

        Args:
            user_id (UUID): The beneficiary's unique ID
        Returns:
            The list of assests if user exists, or None otherwise
        """
        try:
            user = self.sess.query(Beneficiary).filter(
                Beneficiary.uuid_pk == user_id
            ).first()
            if user:
                assets = user.assets
                return assets
            return None
        except DataError:
            return None

    def get_asset(self, user_id: UUID, asset_id: UUID):
        """
        Retrieve an asset.

        Args:
            user_id (UUID): The grantor unique identifier
            asset_id (UUID): The asset unique identifier
        Returns:
            Return asset if successful, None otherwise
        """
        try:
            asset = self.sess.query(Asset).filter_by(
                uuid_pk=asset_id,
                owner_id=user_id
            ).first()
            if asset:
                return asset
            return None
        except DataError:
            return None

    def update_asset(self, user_id: UUID, asset_id: UUID, data):
        """
        Update an asset.

        Args:
            user_id (UUID): The grantor unique identifier
            asset_id (UUID): The asset unique identifier
            data (dict): The data to be updated
        Returns:
            Return True if the update was successful, None otherwise
        """
        try:
            asset = self.sess.query(Asset).filter_by(
                uuid_pk=asset_id,
                owner_id=user_id
            )
            if asset.first():
                asset.update(**data)
                self.sess.commit()
                return True
            return None
        except DataError:
            return None

    def delete_asset(self, user_id: UUID, asset_id: UUID) -> bool | None:
        """
        Delete an asset.

        Args:
            user_id (UUID): The grantor unique identifier
            asset_id (UUID): The asset unique identifier
        Returns:
            True if successful, None otherwise
        """
        try:
            asset = self.sess.query(Asset).filter_by(
                uuid_pk=asset_id,
                owner_id=user_id
            )
            if asset.first():
                asset.delete()
                self.sess.commit()
                return True
            return None
        except DataError:
            return None
