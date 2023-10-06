#!/usr/bin/python3
"""Authenticate API routes for Estate Trust."""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from api.v1.authorizations.oauth import create_token
from api.v1.configurations.database import get_db
from api.v1.models.data.users import User, Trustee
from api.v1.models.schemas.users import SignInUser
from api.v1.utils.passwd import verify_pwd

auths_routers = APIRouter(prefix="/auths", tags=["Authenticate",])


@auths_routers.post("/account/login", status_code=200)
async def login(data: SignInUser, sess: Session = Depends(get_db)):
    """
    Login a user.

    Methods:
        POST
    Args:
        data (dict): Object that contains username and password.
    Returns:
        Status code 200 on successful, otherwise 401.
    """
    if data.account_type == "grantor":
        q_user: User | None = sess.query(User).filter(
            User.username == data.username
        ).first()
    elif data.account_type == "trustee":
        q_user: Trustee | None = sess.query(Trustee).filter(
            Trustee.username == data.username
        ).first()
    try:
        if q_user and verify_pwd(data.password, q_user.password):
            access_token = create_token(
                data={
                    "uuid_pk": q_user.uuid_pk,
                    "username": q_user.username
                }
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "id": q_user.uuid_pk
            }
    except UnboundLocalError as errpr:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account type is required"
        ) from errpr
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
