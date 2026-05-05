from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum


# --- ENUMS ---
class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


class RecurrenceInterval(str, Enum):
    NEVER = "NEVER"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


# --- BASE SCHEMA ---
class TransactionBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    notation: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
    )
    amount: Decimal = Field(
        gt=0,
        max_digits=20,
        decimal_places=2,
    )
    recurrence_interval: RecurrenceInterval = RecurrenceInterval.NEVER
    recurrence_date: Optional[datetime] = None


# --- CREATE ---
class TransactionCreate(TransactionBase):
    wallet_id: int = Field(ge=1)
    type: TransactionType
    category_id: Optional[int] = Field(default=None, ge=1)
    idempotency_key: Optional[str] = Field(
        default=None,
        max_length=64,
    )


# --- CREATE TRANSFER ---
class TransferCreate(BaseModel):
    from_wallet_id: int = Field(ge=1)
    to_wallet_id: int = Field(ge=1)
    amount: Decimal = Field(
        gt=0,
        max_digits=20,
        decimal_places=2,
    )
    name: str = Field(min_length=1, max_length=255)
    idempotency_key: Optional[str] = Field(
        default=None,
        max_length=64,
    )

    @model_validator(mode="after")
    def validate_wallets(self):
        if self.from_wallet_id == self.to_wallet_id:
            raise ValueError("from_wallet_id must be different from to_wallet_id")
        return self


# --- UPDATE ---
class TransactionUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    notation: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
    )
    amount: Optional[Decimal] = Field(
        default=None,
        gt=0,
        max_digits=20,
        decimal_places=2,
    )
    category_id: Optional[int] = Field(default=None, ge=1)
    recurrence_interval: Optional[RecurrenceInterval] = None
    recurrence_date: Optional[datetime] = None



# ---- READ ----
class TransactionRead(TransactionBase):
    id: int = Field(ge=1)
    type: TransactionType
    wallet_id: int
    category_id: Optional[int]
    linked_transaction_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ---- FILTERS ----
class TransactionFilters(BaseModel):
    ids: Optional[List[int]] = Field(default=None, min_length=1, max_length=1000)
    wallet_ids: Optional[List[int]] = Field(default=None, min_length=1, max_length=1000)
    category_ids: Optional[List[int]] = Field(default=None, min_length=1, max_length=1000)
    types: Optional[List[TransactionType]] = None
    amount_min: Optional[Decimal] = Field(default=None, ge=0)
    amount_max: Optional[Decimal] = Field(default=None, ge=0)
    created_at_from: Optional[datetime] = None
    created_at_to: Optional[datetime] = None
    is_transfer: Optional[bool] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=1000)

    @model_validator(mode="after")
    def validate_ranges(self):
        if self.amount_min is not None and self.amount_max is not None:
            if self.amount_min > self.amount_max:
                raise ValueError("amount_min must be <= amount_max")

        if self.created_at_from and self.created_at_to:
            if self.created_at_from > self.created_at_to:
                raise ValueError("created_at_from must be <= created_at_to")

        return self