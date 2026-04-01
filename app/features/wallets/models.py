from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    String,
    DateTime,
    CheckConstraint,
    Numeric,
    Enum,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.postgres.base import Base


class WalletType(str, PyEnum):
    SAVINGS = "SAVINGS"
    SPENDINGS = "SPENDINGS"


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    type: Mapped[WalletType] = mapped_column(
        Enum(
            WalletType,
            name="wallet_type",
            native_enum=False
        ),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )

    initial_balance: Mapped[Decimal] = mapped_column(
        Numeric(20, 2),
        default=Decimal("0.00"),
        server_default="0.00",
        nullable=False
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(20, 2),
        default=Decimal("0.00"),
        server_default="0.00",
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "balance >= 0",
            name="check_balance_non_negative"
        ),
        CheckConstraint(
            "initial_balance >= 0",
            name="check_initial_balance_non_negative"
        ),
    )