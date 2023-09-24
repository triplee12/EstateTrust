#!/usr/bin/python3
"""Users schemas for Estate Trust."""

from datetime import datetime, date
from enum import Enum
from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .assets import AssetRes, MonetaryRes


class Gender(str, Enum):
    """Gender choices."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class BeneficiaryEnum(str, Enum):
    """Beneficiary choices."""

    BROTHER = "brother"
    COUSIN = "cousin"
    DAUGHTER = "daughter"
    FATHER = "father"
    FRIEND = "friend"
    GRAND_CHILD = "grandchild"
    HUSBAND = "husband"
    INLAW = "inlaw"
    MOTHER = "mother"
    NEPHEW = "nephew"
    SISTER = "sister"
    SON = "son"
    STEP_SON = "stepson"
    STEP_DAUGHTER = "stepdaughter"
    WIFE = "wife"


class TrusteeEnum(str, Enum):
    """Trustee choices."""

    BROTHER = "brother"
    FRIEND = "friend"
    LAWYER = "lawyer"
    SISTER = "sister"


class VerifyUser(BaseModel):
    """Verify a user."""

    username: str


class TokenData(BaseModel):
    """Token data schema."""

    uuid_pk: UUID


class AccessToken(BaseModel):
    """Access token schema."""

    token_type: str
    bearer: str


class BaseUser(BaseModel):
    """Base user class."""

    first_name: str
    last_name: str
    middle_name: str


class RegisterUser(BaseUser):
    """Register user derived from BaseUser."""

    username: str
    email: EmailStr
    password: str
    phone_number: str
    date_of_birth: date
    gender: Gender


class SignInUser(BaseModel):
    """Login user into the web or mobile application."""

    username: str
    password: str


class AddTrustee(BaseUser):
    """Create a new trustee/executor for the specified user."""

    username: str
    email: EmailStr
    phone_number: str
    password: str
    relation: TrusteeEnum
    added_by: Optional[str] = ""
    note: Optional[str]


class AddBeneficiary(BaseUser):
    """Create a new beneficiary."""

    relation: BeneficiaryEnum
    added_by: Optional[str] = ""


class BeneficiaryRes(BaseModel):
    """Return all the beneficiaries of a particular user."""

    uuid_pk: str
    first_name: str
    middle_name: str
    last_name: str
    relation: str
    added_by: str
    created_at: datetime
    # updated_at: datetime

    class Config:
        """Serialiser configuration."""

        orm_mode = True


class TrusteeRes(BaseModel):
    """Return all the executors of a particular user."""

    uuid_pk: str
    username: str
    first_name: str
    middle_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    relation: str
    added_by: str
    created_at: datetime
    # updated_at: datetime

    class Config:
        """Serialiser configuration."""

        orm_mode = True


class UserRes(BaseModel):
    """Return all the users in the database."""

    uuid_pk: str
    username: str
    first_name: str
    middle_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    date_of_birth: date
    gender: str
    created_at: datetime
    # updated_at: datetime
    beneficiaries: List[BeneficiaryRes]
    executors: List[TrusteeRes]
    assets: List[AssetRes]
    monetaries: List[MonetaryRes]

    class Config:
        """Serialiser configuration."""

        orm_mode = True


class UpdateUsername(BaseModel):
    """Update username."""

    username: str


class UpdateEmail(BaseModel):
    """Update email."""

    email: EmailStr


class UpdatePassword(BaseModel):
    """Update password."""

    password: str
    password_confirmation: str


class UpdatePhoneNumber(BaseModel):
    """Update phone number."""

    phone_number: str


class UpdateUser(BaseModel):
    """Update a user details."""

    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[Gender]
    updated_at: str = datetime.now()


class UpdateTrustee(BaseModel):
    """Update trustee information."""

    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    relation: Optional[TrusteeEnum]
    note: Optional[str]
    updated_at: str = datetime.now()


class UpdateBeneficiary(BaseModel):
    """Update beneficiary information."""

    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    relation: Optional[BeneficiaryEnum]
    updated_at: str = datetime.now()
