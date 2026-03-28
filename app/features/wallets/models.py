from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import String, Float, DateTime, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class WalletType(str, Enum):
    SAVINGS = "SAVINGS"
    SPENDINGS = "SPENDINGS"


class TransactionType(str, Enum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"


class RepeatTimeType(str, Enum):
    NEVER = "NEVER"
    EVERY_DAY = "EVERY_DAY"
    EVERY_MONTH = "EVERY_MONTH"
    EVERY_YEAR = "EVERY_YEAR"



class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[WalletType] = mapped_column(
        Enum(WalletType, name="wallet_type"),
        nullable=False
    )
    init_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False
    )
    init_balance: Mapped[float] = mapped_column(Float, default=0)
    balance: Mapped[float] = mapped_column(Float, default=0)

    # ==========================
    # RELATIONS
    # ==========================

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="wallet",
        cascade="all, delete-orphan"
    )

    categories: Mapped[list["Category"]] = relationship(
        back_populates="wallet",
        cascade="all, delete-orphan"
    )

    stats_total: Mapped["StatsWalletTotal"] = relationship(
        back_populates="wallet",
        uselist=False  # one-to-one
    )

    daily_category_stats: Mapped[list["StatsDailyCategory"]] = relationship(
        back_populates="wallet"
    )

    # ==========================
    # INDEXES
    # ==========================

    __table_args__ = (
        Index("ix_wallet_type", "type"),
    )