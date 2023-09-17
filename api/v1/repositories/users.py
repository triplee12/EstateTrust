#!/usr/bin/python3
"""Users repository for Estate Trust."""

from typing import Any, Dict, List
from uuid import UUID
from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from api.v1.configurations.database import get_db
from api.v1.models.data.users import User


class UserRepository:
    """User repository for Estate Trust."""

    def __init__(self, sess: Session = Depends(get_db)) -> None:
        """Initialize the repository."""
        self.sess: Session = sess

    def insert_user(self, user: User) -> bool:
        """Insert a user into the database."""
        try:
            self.sess.add(user)
            self.sess.commit()
        except IntegrityError:
            return False
        return True

    def retrieve_user(self, uuid_pk: UUID) -> User | None:
        """Retrieve the user associated with the given uuid."""
        try:
            user: User | None = self.sess.query(User).filter(
                User.uuid_pk == uuid_pk
            ).one_or_none()
        except DataError:
            return None
        return user

    def retrieve_users(self) -> List[User]:
        """Retrieve users."""
        users: List[User] = self.sess.query(User).all()
        return users

    def retrieve_users_sorted_desc(self) -> List[User]:
        """Retrieve all the users in descending order."""
        users: List[User] = self.sess.query(User).order_by(
            desc(User.username)
        ).all()
        return users

    def update_user(self, uuid_pk: UUID, data: Dict[str, Any]) -> bool:
        """Update a user data in the database."""
        try:
            user = self.sess.query(User).filter(User.uuid_pk == uuid_pk)
            if user.one():
                user.update(data)
                self.sess.commit()
                return True
            return False
        except DataError:
            return False

    def delete_user(self, uuid_pk: UUID):
        """Delete user."""
        try:
            user = self.sess.query(User).filter(User.uuid_pk == uuid_pk)
            if user.one():
                user.delete()
                self.sess.commit()
                return True
            return False
        except DataError:
            return False
