from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    String,
    DateTime,
    Numeric,
    UniqueConstraint,
    func,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgres.base import Base


class WalletType(str, PyEnum):
    """Defines the purpose of the wallet."""

    SAVINGS = "SAVINGS"
    SPENDINGS = "SPENDINGS"


class Wallet(Base):
    """User's financial wallet (Bank Card)"""

    __tablename__ = "wallets"

    # --- Fields ---
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[WalletType] = mapped_column(
        SQLEnum(WalletType, name="wallet_type_enum", native_enum=True), nullable=False
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), server_default="0.00", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(), # update time python side
        nullable=False,
    )

    # --- Relationships ---
    categories: Mapped[List["Category"]] = relationship(
        "Category",
        back_populates="wallet",
        cascade="all, delete-orphan",
        lazy="selectin", # categories few
    )
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="wallet",
        cascade="all, delete-orphan",
        lazy="noload", # transactions many
    )

    # --- Table Arguments ---
    __table_args__ = (
        UniqueConstraint("name", name="wallet_name"),
    )