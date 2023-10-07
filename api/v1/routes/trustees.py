#!/usr/bin/python3
"""Trustees routers for Estate Trust."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from api.v1.authorizations.oauth import get_current_user
from api.v1.configurations.database import get_db
from api.v1.models.data.users import Trustee, User
from api.v1.models.schemas.users import (
    AddTrustee, TrusteeRes, UpdateTrustee
)
from api.v1.repositories.trustees import TrusteeRepository
from api.v1.utils.passwd import hash_pwd

trustee_router = APIRouter(prefix="/trustees", tags=["trustees"])


@trustee_router.post(
    "/account/{grantor_id}/create/trustee",
    status_code=status.HTTP_201_CREATED
)
async def create_trustee(
    grantor_id: str,
    trustee: AddTrustee,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Create a new trustee."""
    repo = TrusteeRepository(sess)
    get_grantor = sess.query(User).filter(User.uuid_pk == grantor_id).first()
    if get_grantor and current_user.uuid_pk == grantor_id:
        trustee.added_by = get_grantor.uuid_pk
        trustee.password = hash_pwd(trustee.password)
        add_trustee = repo.add_trustee(trustee)
        if add_trustee:
            return {
                "message": "Trustee added successfully"
            }
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User with {trustee.username} already exists"
        )


@trustee_router.get(
    "/account/{grantor_id}/trustees/{trustee_id}",
    response_model=TrusteeRes
)
async def retrieve_trustee(
    grantor_id: str, trustee_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Retrieve the specified trustee for the specified grantor."""
    repo = TrusteeRepository(sess)
    if current_user.uuid_pk == grantor_id:
        trustee = repo.get_trustee(trustee_id=trustee_id, user_id=grantor_id)
        if trustee:
            return trustee
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="trustee not found"
        )


@trustee_router.get(
    "/account/{grantor_id}/trustees",
    response_model=List[TrusteeRes]
)
async def retrieve_trustees(
    grantor_id, current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Retrieve the list of trustees for the given grantor."""
    repo = TrusteeRepository(sess)
    if current_user.uuid_pk == grantor_id:
        trustees = repo.get_trustees(user_id=grantor_id)
        if len(trustees) == 0:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="You do not have any trustees"
            )
        return trustees


@trustee_router.put(
    "/account/{grantor_id}/trustees/{trustee_id}/update",
    response_model=TrusteeRes
)
async def update_trustee_account(
    grantor_id, trustee_id, data: UpdateTrustee,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Update the trustee data for the specified grantor."""
    repo = TrusteeRepository(sess)
    if current_user.uuid_pk == grantor_id:
        trustee = repo.update_trustee(
            user_id=grantor_id,
            trustee_id=trustee_id, data=data
        )
        if trustee:
            return trustee
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="error occurred while updating trustee data"
        )


@trustee_router.delete("/account/{grantor_id}/trustees/{trustee_id}/delete")
async def delete_trustee_account(
    grantor_id: str, trustee_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Delete a trustee account from the database."""
    repo = TrusteeRepository(sess)
    if current_user.uuid_pk == grantor_id:
        del_trustee = repo.delete_trustee(
            user_id=grantor_id, trustee_id=trustee_id
        )
        if not del_trustee:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="error occurred while deleting trustee account"
            )
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="account deleted successfully"
        )


@trustee_router.get(
    "/account/trustee/{trustee_id}/dashboard",
    response_model=TrusteeRes
)
async def trustee_dashboard(
    trustee_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """Trustee dashboard with unlimited access."""
    if current_user.uuid_pk == trustee_id:
        q_trustee = sess.query(Trustee).filter(
            Trustee.uuid_pk == trustee_id
        ).first()
        return q_trustee
