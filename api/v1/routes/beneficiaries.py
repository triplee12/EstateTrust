#!/usr/bin/python3
"""Beneficiaries router for Estate Trust."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from api.v1.authorizations.oauth import get_current_user
from api.v1.configurations.database import get_db
from api.v1.models.data.users import User
from api.v1.models.schemas.users import (
    AddBeneficiary, BeneficiaryRes, UpdateBeneficiary
)
from api.v1.repositories.beneficiaries import BeneficiaryRepo

beneficiary_router = APIRouter(
    prefix="/beneficiaries",
    tags=["beneficiaries", "Beneficiary"]
)


@beneficiary_router.post(
    "/account/{grantor_id}/create/beneficiary",
    status_code=status.HTTP_201_CREATED
)
async def create_beneficiary(
    grantor_id: str, data: AddBeneficiary,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Add new beneficiary to the database.

    Method: POST
    Args:
        data (dict): dictionary containing beneficiary's information
    Returns:
        return 201 if successful, 422 otherwise
    """
    repo = BeneficiaryRepo(sess)
    if current_user.uuid_pk == grantor_id:
        grantor = sess.query(User).filter(User.uuid_pk == grantor_id).first()
        data.added_by = grantor.uuid_pk
        add_beneficiary = repo.add_beneficiary(data)
        if add_beneficiary:
            return {
                "message": "Beneficiary added successfully"
            }
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="error occurred while adding beneficiary"
        )


@beneficiary_router.get(
    "/account/{user_id}/beneficiaries",
    response_model=List[BeneficiaryRes]
)
async def retrieve_beneficiaries(
    user_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Retrieve all the beneficiaries information associated with a given grantor.

    Method: GET
    Args:
        user_id (str): ID of the grantor
    Returns:
        list of beneficiaries information
    """
    repo = BeneficiaryRepo(sess)
    if current_user.uuid_pk == user_id:
        beneficiaries = repo.get_all_beneficiaries(user_id=user_id)
        if beneficiaries:
            return beneficiaries
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="no beneficiaries found"
        )


@beneficiary_router.get(
    "/account/{user_id}/beneficiaries/{bene_id}",
    response_model=BeneficiaryRes
)
async def get_beneficiary(
    user_id: str, bene_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Retrieve a beneficiary information for a given user.

    Method: GET
    Args:
        user_id (str): ID of the grantor
        bene_id (str): ID of the beneficiary
    Returns:
        dictionary of beneficiary's information
    """
    repo = BeneficiaryRepo(sess)
    if current_user.uuid_pk == user_id:
        beneficiary = repo.get_beneficiary(
            uuid_pk=bene_id, added_by=user_id
        )
        if beneficiary:
            return beneficiary
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="beneficiary not found"
        )


@beneficiary_router.put(
    "/account/{grantor_id}/beneficiaries/{bene_id}/update",
    response_model=BeneficiaryRes
)
async def update_beneficiary(
    grantor_id: str, bene_id: str, data: UpdateBeneficiary,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Update the beneficiary data in the database.

    Method: PATCH
    Args:
        grantor_id (str): ID of the grantor
        bene_id (str): ID of the beneficiary
        data: dictionary containing beneficiary's data to update
    Returns:
        dictionary of beneficiary's information
    """
    repo = BeneficiaryRepo(sess)
    if current_user.uuid_pk == grantor_id:
        beneficiary = repo.update_beneficiary(
            added_by=grantor_id, uuid_pk=bene_id, data=data
        )
        if beneficiary:
            return beneficiary
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="error occurred while updating beneficiary"
        )


@beneficiary_router.delete(
    "/account/{grantor_id}/beneficiaries/{bene_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_beneficiary(
    grantor_id: str, bene_id: str,
    current_user: str = Depends(get_current_user),
    sess: Session = Depends(get_db)
):
    """
    Delete a beneficiary from the database.

    Method: DELETE
    Args:
        grantor_id (str): ID of the grantor
        bene_id (str): ID of the beneficiary
    Returns:
        return 204 on success, 304 on failure
    """
    repo = BeneficiaryRepo(sess)
    if current_user.uuid_pk == grantor_id:
        del_beneficiary = repo.delete_beneficiary(
            added_by=grantor_id, uuid_pk=bene_id
        )
        if not del_beneficiary:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="error occurred while deleting beneficiary"
            )
