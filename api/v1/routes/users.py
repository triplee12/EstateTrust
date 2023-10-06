#!/usr/bin/python3
"""Users API routes for Estate Trust."""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from api.v1.authorizations.oauth import get_current_user
from api.v1.configurations.database import get_db
from api.v1.models.schemas.users import (
    RegisterUser, UserRes, UpdateUser
)
from api.v1.repositories.users import UserRepository
from api.v1.utils.passwd import hash_pwd

user_routers = APIRouter(prefix="/grantors", tags=["grantor",])


@user_routers.post("/account/create", status_code=201)
async def create_grantor_account(
    grantor: RegisterUser,
    sess: Session = Depends(get_db)
):
    """
    Create grantor account.

    Methods:
        POST
    Args:
        grantor (dict): Object that contains the account information.
    Returns:
        Status code 201 on successful, otherwise 422.
    """
    repo = UserRepository(sess)
    password = hash_pwd(grantor.password)
    grantor.password = password
    data: bool = repo.insert_user(grantor)
    if data:
        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "Account created successfully"
        }
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Error creating account."
    )


@user_routers.get("/account/dashboard/{uuid_pk}", response_model=UserRes)
async def get_dashboard(
    uuid_pk: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Retrieve grantor's dashboard."""
    repo = UserRepository(sess)
    if current_user.uuid_pk == uuid_pk:
        grantor = repo.retrieve_user(uuid_pk=current_user.uuid_pk)
        if grantor:
            return grantor
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


@user_routers.put(
    "/account/dashboard/{uuid_pk}/update",
    response_model=UserRes
)
async def update_account(
    uuid_pk: str, data: UpdateUser,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Update grantor account."""
    repo = UserRepository(sess)
    if current_user.uuid_pk == uuid_pk:
        update = repo.update_user(uuid_pk=current_user.uuid_pk, data=data)
        if update:
            return update
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="error updating account"
            )


@user_routers.delete(
    "/account/dashboard/{uuid_pk}/delete",
    status_code=204
)
async def delete_account(
    uuid_pk: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Delete a user account."""
    repo = UserRepository(sess)
    if current_user.uuid_pk == uuid_pk:
        deleted = repo.delete_user(current_user.uuid_pk)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error deleting account"
            )
