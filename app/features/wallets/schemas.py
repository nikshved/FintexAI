from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from app.features.wallets.models import WalletType


# --- BASE SCHEMA ---
class WalletBase(BaseModel):
    name: str = Field(
        min_length=1, max_length=255, pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-_]+$"
    )
    type: WalletType


# --- READ SCHEMA (Response) ---
class WalletRead(BaseModel):
    id: int = Field(ge=1)
    name: str
    type: WalletType
    balance: Decimal = Field(ge=0, max_digits=20, decimal_places=2)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- CREATE SCHEMA ---
class WalletCreate(WalletBase):
    pass


# --- UPDATE SCHEMA ---
class WalletUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-_]+$",
    )
    type: Optional[WalletType] = None


# --- BULK OPERATIONS ---
class WalletsCreate(BaseModel):
    wallets: List[WalletCreate] = Field(min_length=1, max_length=1000)


class WalletsUpdateItem(BaseModel):
    id: int = Field(ge=1)
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-_]+$",
    )
    type: Optional[WalletType] = None


class WalletsUpdate(BaseModel):
    wallets: List[WalletsUpdateItem] = Field(min_length=1, max_length=1000)

    @field_validator("wallets")
    @classmethod
    def ids_must_be_unique(cls, v):
        ids = [item.id for item in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Wallet ids must be unique")
        return v


class WalletsDelete(BaseModel):
    ids: List[int] = Field(min_length=1, max_length=1000)

    @field_validator("ids")
    @classmethod
    def ids_must_be_unique(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("ids must be unique")
        return v


# --- FILTERS & PAGINATION ---
class WalletFilters(BaseModel):
    ids: Optional[List[int]] = Field(default=None, min_length=1, max_length=1000)
    names: Optional[List[str]] = Field(default=None, min_length=1, max_length=1000)
    types: Optional[List[WalletType]] = Field(default=None, min_length=1)

    balance_min: Optional[Decimal] = Field(default=None, ge=0)
    balance_max: Optional[Decimal] = Field(default=None, ge=0)

    created_at_from: Optional[datetime] = None
    created_at_to: Optional[datetime] = None

    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=1000)

    @model_validator(mode="after")
    def validate_ranges(self):
        if self.balance_min is not None and self.balance_max is not None:
            if self.balance_min > self.balance_max:
                raise ValueError("balance_min must be <= balance_max")
        if self.created_at_from is not None and self.created_at_to is not None:
            if self.created_at_from > self.created_at_to:
                raise ValueError("created_at_from must be <= created_at_to")
        return self