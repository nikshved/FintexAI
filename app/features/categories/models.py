from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import (
    String,
    DateTime,
    Numeric,
    func,
    ForeignKey,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgres.base import Base
from app.features.transactions.models import Transaction
from app.features.wallets.models import Wallet

class Category(Base):
    __tablename__ = "categories"

    # --- Fields ---
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    notation: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Base budget limit for the category
    limit: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), server_default="0.00", nullable=False
    )

    init_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )

    # --- Foreign Keys ---
    wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False
    )

    # --- Relationships ---
    wallet: Mapped["Wallet"] = relationship(
        "Wallet",
        back_populates="categories",
        lazy="selectin"
    ) 
    transactions: Mapped[List[Transaction]] = relationship( 
        Transaction,
        back_populates="categories",
        cascade="all, delete-orphan",
        lazy="noload"
    )

    # --- Constraints & Indexes ---
    __table_args__ = (
        CheckConstraint("limit >= 0", name="check_category_limit_non_negative"),
        Index("ix_category_wallet_id", "wallet_id"),
    )
