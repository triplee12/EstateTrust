#!/usr/bin/python3
"""Users models for estate planning software."""

from sqlalchemy import (
    Column, String, DateTime, Enum, Text,
    TIMESTAMP, ForeignKey, text, Date
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from api.v1.configurations.database import Base

# PostgreSQL UUID type
PgUUID = UUID(as_uuid=False)


class User(Base):
    """User model for estate planning software."""

    __tablename__: str = 'users'
    # Generate random UUID primary key column
    uuid_pk = Column(
        PgUUID, primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    username = Column(String(10), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    phone_number = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(
        Enum(
            "female", "male", "other",
            name="gender_enum",
            create_type=False
        ), nullable=False
    )
    beneficiaries = relationship(
        "Beneficiary", back_populates="user"
    )
    executors = relationship(
        "Trustee", back_populates="user"
    )
    assets = relationship(
        "Asset", back_populates="owner"
    )
    monetaries = relationship(
        "Monetary", back_populates="owner"
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )
    updated_at = Column(
        "updated_at", DateTime(timezone=True),
        default=None, index=False
    )

    def __repr__(self) -> str:
        """User representation."""
        return f"{self.username} - {self.last_name} - {self.created_at}"

    def __str__(self) -> str:
        """User representation."""
        return f"{self.username} - {self.last_name} - {self.created_at}"


class Beneficiary(Base):
    """Beneficiary model."""

    __tablename__: str = 'beneficiaries'
    uuid_pk = Column(
        PgUUID, primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    relation = Column(
        Enum(
            "brother", "sister", "son", "daughter",
            "wife", "husband", "stepson", "stepdaughter",
            "grandchild", "cousin", "nephew", "friend",
            "father", "mother", "inlaw",
            name="rela_enum",
            create_type=False
        ), nullable=False
    )
    added_by = Column(
        PgUUID,
        ForeignKey("users.uuid_pk", ondelete="CASCADE"),
        nullable=False
    )
    user = relationship(
        "User", back_populates="beneficiaries",
        foreign_keys=added_by
    )
    assets = relationship(
        "Asset", back_populates="beneficiary"
    )
    money = relationship(
        "Monetary", back_populates="beneficiary"
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )
    updated_at = Column(
        "updated_at", DateTime(timezone=True),
        default=None, index=False
    )

    def __str__(self):
        """Beneficiary representation."""
        return f"{self.first_name} - {self.last_name}"


class Trustee(Base):
    """User trustee model."""

    __tablename__: str = 'trustees'
    uuid_pk = Column(
        PgUUID, primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    username = Column(String(10), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    email = Column(String(150), nullable=False)
    phone_number = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    relation = Column(
        Enum(
            "brother", "sister", "friend", "lawyer",
            "wife", name="executor_enum",
            create_type=False
        ), nullable=False
    )
    added_by = Column(
        PgUUID,
        ForeignKey("users.uuid_pk", ondelete="CASCADE"),
        nullable=False
    )
    user = relationship(
        "User", back_populates="executors",
        foreign_keys=[added_by]
    )
    note = Column(Text, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )
    updated_at = Column(
        "updated_at", DateTime(timezone=True),
        default=None, index=False
    )

    def __str__(self):
        """Trustee representation."""
        return f"{self.username} - {self.first_name} - {self.last_name}"
