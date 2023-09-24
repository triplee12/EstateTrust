#!/usr/bin/python3
"""Assets schemas for Estate Trust."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AddAsset(BaseModel):
    """Create physical asset."""

    name: str
    location: Optional[str] = ""
    owner_id: Optional[str] = ""
    will_to: str
    note: Optional[str]


class AddMonetary(BaseModel):
    """Create monetary assest."""

    acc_name: str
    acc_number: str
    amount: str
    bank_name: str
    owner_id: Optional[str] = ""
    will_to: str
    note: Optional[str]


class AssetRes(BaseModel):
    """Return asset data."""

    uuid_pk: str
    name: str
    location: str
    owner_id: str
    will_to: str
    note: str
    created_at: datetime
    # updated_at: datetime

    class Config:
        """Serialiser configuration."""

        orm_mode = True


class MonetaryRes(BaseModel):
    """Return monetary data."""

    uuid_pk: str
    acc_name: str
    acc_number: str
    amount: str
    bank_name: str
    owner_id: str
    will_to: str
    note: str
    created_at: datetime
    # updated_at: datetime

    class Config:
        """Serialiser configuration."""

        orm_mode = True


class UpdateAsset(BaseModel):
    """Update asset model data."""

    name: Optional[str]
    location: Optional[str]
    will_to: Optional[str]
    note: Optional[str]
    updated_at: str = datetime.now()


class UpdateMonetary(BaseModel):
    """Update monetary model date."""

    acc_name: Optional[str]
    acc_number: Optional[str]
    amount: Optional[str]
    bank_name: Optional[str]
    will_to: Optional[str]
    note: Optional[str]
    updated_at: str = datetime.now()
