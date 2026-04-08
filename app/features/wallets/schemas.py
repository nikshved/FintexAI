from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum


# --- ENUMS ---
class WalletType(str, Enum):
    SAVINGS = "SAVINGS"
    SPENDINGS = "SPENDINGS"


# --- BASE SCHEMA ---
class WalletBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: WalletType


# --- READ SCHEMA (Response) ---
class WalletRead(WalletBase):
    id: int
    balance: Decimal = Field(max_digits=20, decimal_places=2)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- CREATE SCHEMA ---
class WalletCreate(WalletBase):
    balance: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=20, decimal_places=2)


# --- UPDATE SCHEMA ---
class WalletUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    type: Optional[WalletType] = None


# --- BULK OPERATIONS ---
class WalletsCreate(BaseModel):
    wallets: List[WalletCreate] = Field(min_length=1)


class WalletsUpdateItem(WalletUpdate):
    id: int


class WalletsUpdate(BaseModel):
    wallets: List[WalletsUpdateItem] = Field(min_length=1)


class WalletsDelete(BaseModel):
    ids: List[int] = Field(min_length=1)


# --- FILTERS & PAGINATION ---
class WalletFilters(BaseModel):
    ids: Optional[List[int]] = None
    names: Optional[List[str]] = None
    types: Optional[List[WalletType]] = None

    balance_min: Optional[Decimal] = None
    balance_max: Optional[Decimal] = None

    created_at_from: Optional[datetime] = None
    created_at_to: Optional[datetime] = None

    # Pagination 
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=1000)

    # Analytics 
    with_stats: bool = False
    stats_date_from: Optional[datetime] = None
    stats_date_to: Optional[datetime] = None