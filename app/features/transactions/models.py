from datetime import datetime
from decimal import Decimal
from typing import Optional
from enum import Enum as PyEnum

from sqlalchemy import (
    String,
    DateTime,
    Numeric,
    func,
    ForeignKey,
    Index,
    Integer,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgres.base import Base


class TransactionType(str, PyEnum):
    """Operation types for financial movements"""
    
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"


class RepeatTimeType(str, PyEnum):
    """Recurring intervals for transactions"""

    NEVER = "NEVER"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"


class Transaction(Base):
    """Financial record tracking all wallet movements"""

    __tablename__ = "transactions"

    # --- Fields ---
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    type: Mapped[TransactionType] = mapped_column(
        SQLEnum(
            TransactionType, name="transaction_operation_type_enum", native_enum=False
        ),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False)

    # Snapshot of the category limit at creation time
    category_limit_snapshot: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), server_default="0.00", nullable=False
    )

    notation: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    init_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    repeat_time: Mapped[RepeatTimeType] = mapped_column(
        SQLEnum(RepeatTimeType, name="transaction_repeat_enum", native_enum=False),
        server_default=RepeatTimeType.NEVER.value,
        nullable=False,
    )

    # --- Foreign Keys ---
    wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )

    # Reference to link a pair of transfer transactions
    linked_transaction_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("transactions.id", ondelete="SET NULL"), nullable=True
    )

    # --- Relationships ---
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="transactions")  # type: ignore
    category: Mapped["Category"] = relationship(  # type: ignore
        "Category", back_populates="transactions"
    )

    linked_transaction: Mapped[Optional["Transaction"]] = relationship(
        "Transaction", remote_side=[id], post_update=True
    )

    # --- Constraints & Indexes ---
    __table_args__ = (
        Index("ix_transaction_wallet_date", "wallet_id", "init_date"),
        Index("ix_transaction_category_date", "category_id", "init_date"),
    )
