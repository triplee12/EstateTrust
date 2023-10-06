#!/usr/bin/python3
"""Assets models for estate planning software."""

from sqlalchemy import (
    Column, String, DateTime, Text,
    TIMESTAMP, ForeignKey, text
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from api.v1.configurations.database import Base

# PostgreSQL UUID type
PgUUID = UUID(as_uuid=False)


class Asset(Base):
    """Asset model."""

    __tablename__: str = 'assets'
    uuid_pk = Column(
        PgUUID, primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    owner_id = Column(
        PgUUID,
        ForeignKey("users.uuid_pk", ondelete="CASCADE"),
        nullable=False
    )
    document = Column(String(255), nullable=True)
    will_to = Column(
        PgUUID,
        ForeignKey("beneficiaries.uuid_pk", ondelete="CASCADE"),
        nullable=False
    )
    owner = relationship(
        "User", back_populates="assets",
        foreign_keys=[owner_id]
    )
    beneficiary = relationship(
        "Beneficiary", back_populates="assets",
        foreign_keys=[will_to]
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

    def __repr__(self):
        """Asset representation."""
        return f"{self.uuid_pk} - {self.name} - {self.will_to}"


class Monetary(Base):
    """Monetary model."""

    __tablename__ = 'monetaries'
    uuid_pk = Column(
        PgUUID, primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    acc_name = Column(String(255), nullable=False)
    acc_number = Column(String(150), nullable=False)
    amount = Column(String(150), nullable=False)
    bank_name = Column(String(255), nullable=False)
    document = Column(String(255), nullable=True)
    owner_id = Column(
        PgUUID,
        ForeignKey("users.uuid_pk", ondelete="CASCADE"),
        nullable=False
    )
    will_to = Column(
        PgUUID,
        ForeignKey("beneficiaries.uuid_pk", ondelete="CASCADE"),
        nullable=False
    )
    owner = relationship(
        "User", back_populates="monetaries",
        foreign_keys=[owner_id]
    )
    beneficiary = relationship(
        "Beneficiary", back_populates="money",
        foreign_keys=[will_to]
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

    def __repr__(self):
        """Monetary representation."""
        return f"{self.uuid_pk} - {self.amount} - {self.will_to}"
