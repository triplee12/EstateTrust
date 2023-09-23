#!/usr/bin/python3
"""Trustees repository for Estate Trust."""

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from api.v1.models.data.users import Trustee, User


class TrusteeRepository:
    """Trustee repository."""

    def __init__(self, sess: Session) -> None:
        """Initialize the trustee repository."""
        self.sess: Session = sess

    def add_trustee(self, data) -> bool:
        """
        Add a new trustee.

        Args:
            data: A dictionary containing the data
        Returns:
            Return True if successful, False otherwise
        """
        try:
            trustee = Trustee(**data.dict())
            self.sess.add(trustee)
            self.sess.commit()
            return True
        except IntegrityError:
            return False

    def get_trustee(self, trustee_id: UUID, user_id: UUID) -> Trustee | None:
        """
        Retrieve a specific trustee.

        Args:
            trustee_id (UUID): The identifier of the trustee to retrieve
            user_id (UUID): The identifier of the user that added the trustee
        Returns:
            The trustee information
        """
        try:
            trustee = self.sess.query(Trustee).filter_by(
                added_by=user_id,
                uuid_pk=trustee_id
            ).first()
            if trustee:
                return trustee
            return None
        except DataError:
            return None

    def get_trustees(self, user_id) -> List[Trustee]:
        """
        Get the list of trustees for a given user.

        Args:
            user_id: The ID of the user that added the trustees
        Returns:
            list of Trustees
        """
        user = self.sess.query(User).filter(User.uuid_pk == user_id).first()
        truestees = user.executors
        return truestees

    def update_trustee(self, user_id: UUID, trustee_id: UUID, data):
        """
        Update a trustee data.

        Args:
            user_id (UUID): The identifier of the user that added the trustee
            trustee_id (UUID): The identifier of the trustee to update
            data (dict): The dictionary containing data to update
        Returns:
            Return True if successful, False otherwise
        """
        try:
            trustee = self.sess.query(Trustee).filter_by(
                uuid_id=trustee_id,
                added_by=user_id
            )
            if trustee.first():
                trustee.update(data.dict(), synchronize_session=False)
                self.sess.commit()
                return trustee.first()
            return False
        except IntegrityError:
            return False
        except DataError:
            return None

    def delete_trustee(self, user_id: UUID, trustee_id: UUID) -> bool:
        """
        Delete a trustee.

        Args:
            user_id (UUID): The identifier of the user that added the trustee
            trustee_id (UUID): The identifier of the trustee to delete
        Returns:
            Return True if successful, False otherwise
        """
        try:
            trustee = self.sess.query(Trustee).filter_by(
                uuid_id=trustee_id,
                added_by=user_id
            )
            if trustee.first():
                trustee.delete()
                self.sess.commit()
                return True
            return False
        except DataError:
            return None
