#!/usr/bin/python3
"""Beneficiaries repository for Estate Trust."""

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from api.v1.models.data.users import Beneficiary, User


class BeneficiaryRepo:
    """Beneficiary repository."""

    def __init__(self, sess: Session) -> None:
        """Initialize the repository."""
        self.sess: Session = sess

    def add_beneficiary(self, beneficiary: Beneficiary) -> bool:
        """Add a beneficiary."""
        benef = Beneficiary(**beneficiary.dict())
        self.sess.add(benef)
        self.sess.commit()
        return True

    def get_beneficiary(
        self, uuid_pk: UUID, added_by: UUID
    ) -> Beneficiary | None:
        """Retrieve a beneficiary for a given user."""
        beneficiary = self.sess.query(Beneficiary).filter_by(
            added_by=added_by,
            uuid_pk=uuid_pk
        ).first()
        if beneficiary:
            return beneficiary
        return None

    def get_all_beneficiaries(self, user_id: UUID) -> List[Beneficiary]:
        """Retrieve all beneficiaries for a given user."""
        user: User | None = self.sess.query(User).filter_by(
            uuid_pk=user_id
        ).first()
        if user:
            beneficiaries = user.beneficiaries
            return beneficiaries

    def update_beneficiary(self, added_by: UUID, uuid_pk: UUID, data):
        """Update a beneficiary data."""
        try:
            beneficiary = self.sess.query(Beneficiary).filter_by(
                added_by=added_by,
                uuid_pk=uuid_pk
            )
            if beneficiary.one():
                beneficiary.update(data.dict(), synchronize_session=False)
                self.sess.commit()
                return beneficiary.one()
            return None
        except DataError:
            return None

    def delete_beneficiary(self, added_by: UUID, uuid_pk: UUID):
        """Delete a beneficiary."""
        try:
            beneficiary = self.sess.query(Beneficiary).filter_by(
                added_by=added_by,
                uuid_pk=uuid_pk
            )
            if beneficiary.one():
                beneficiary.delete()
                self.sess.commit()
                return True
            return None
        except DataError:
            return None
