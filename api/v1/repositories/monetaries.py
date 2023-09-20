#!/usr/bin/python3
"""Monetaries repository for Estate Trust."""

from typing import List
from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from api.v1.configurations.database import get_db
from api.v1.models.data.users import Beneficiary, User
from api.v1.models.data.assets import Monetary


class MonetaryRepository:
    """Monetary repository."""

    def __init__(self, sess: Session = Depends(get_db)) -> None:
        """Initialize the repository."""
        self.sess: Session = sess

    def add_monetary_asset(self, data) -> bool:
        """
        Add a new monetary asset.

        Args:
            data (dict): The data to add
        Returns:
            return True if successful, False otherwise
        """
        try:
            asset = Monetary(*data)
            self.sess.add(asset)
            self.sess.commit()
            return True
        except IntegrityError:
            return False

    def get_all_monetary_assets_for_grantor(
        self, grantor_id: UUID
    ) -> List[Monetary] | None:
        """
        Retrieve all the assets for a given grantor.

        Args:
            grantor_id (UUID): The grantor unique identifier
        Returns:
            Return list of monetary assets, None otherwise.
        """
        try:
            user = self.sess.query(User).filter(
                User.uuid_pk == grantor_id
            ).first()
            monetaries = user.monetaries
            return monetaries
        except DataError:
            return None

    def get_all_monetary_assets_for_beneficiary(
        self, will_to: UUID
    ) -> List[Monetary] | None:
        """
        Retrieve all the monetary assets for a beneficiary.

        Args:
            will_to (UUID): The beneficiary unique identifier
        Returns:
            Return list of monetary assets, None otherwise.
        """
        try:
            beneficiary = self.sess.query(Beneficiary).filter_by(
                uuid_pk=will_to
            ).first()
            monetaries = beneficiary.money
            return monetaries
        except DataError:
            return None

    def get_asset(self, grantor_id: UUID, asset_id: UUID) -> Monetary | None:
        """
        Retrieve a monetary asset data.

        Args:
            grantor_id (UUID): The grantor unique identifier
            asset_id (UUID): The asset identifier
        Returns:
            Return monetary, None otherwise
        """
        try:
            monetary = self.sess.query(Monetary).filter_by(
                owner_id=grantor_id,
                uuid_pk=asset_id
            ).first()
            return monetary
        except DataError:
            return None

    def update_asset(self, grantor_id: UUID, asset_id: UUID, data) -> bool:
        """
        Update monetary asset data.

        Args:
            grantor_id (UUID): The grantor unique identifier
            asset_id (UUID): The asset identifier
            data (dict): The data to be updated
        Returns:
            Return True if the asset was successfully updated, False otherwise
        """
        try:
            monetary = self.sess.query(Monetary).filter_by(
                owner_id=grantor_id,
                uuid_pk=asset_id
            )
            monetary.update(**data)
            self.sess.commit()
            return True
        except DataError:
            return False

    def delete_asset(self, grantor_id: UUID, asset_id: UUID) -> bool:
        """
        Delete monetary asset data.

        Args:
            grantor_id (UUID): The grantor unique identifier
            asset_id (UUID): The asset identifier
        Returns:
            Return True if the asset was successfully deleted, False otherwise
        """
        try:
            monetary = self.sess.query(Monetary).filter_by(
                owner_id=grantor_id,
                uuid_pk=asset_id
            )
            monetary.delete()
            self.sess.commit()
            return True
        except DataError:
            return False
