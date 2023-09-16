#!/usr/bin/python3
"""Password utility functions."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str) -> CryptContext:
    """Hash password."""
    return pwd_context.hash(password)


def verify_pwd(password: str, hashed_password: str) -> CryptContext:
    """Verify password."""
    return pwd_context.verify(password, hashed_password)
