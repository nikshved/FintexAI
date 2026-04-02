from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum


# ===== ENUM =====

class WalletType(str, Enum):
    SAVINGS = "SAVINGS"
    SPENDINGS = "SPENDINGS"


# ===== BASE =====

class WalletBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: WalletType


# ===== READ (response) =====

class WalletRead(WalletBase):
    id: int
    balance: Decimal
    initial_balance: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ===== CREATE =====

class WalletCreate(WalletBase):
    initial_balance: Decimal = Field(default=Decimal("0.00"), ge=0)


# ===== UPDATE =====

class WalletUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    type: Optional[WalletType] = None
    initial_balance: Optional[Decimal] = Field(default=None, ge=0)

# ***** BULK OPERATIONS *****

# ===== BULK CREATE =====

class WalletsCreate(BaseModel):
    wallets: List[WalletCreate] = Field(min_items=1)


# ===== BULK UPDATE =====

class WalletsUpdateItem(WalletUpdate):
    id: int


class WalletsUpdate(BaseModel):
    wallets: List[WalletsUpdateItem] = Field(min_items=1)


# ===== DELETE =====

class WalletsDelete(BaseModel):
    ids: List[int] = Field(min_items=1)


# ===== FILTERS =====

class WalletFilters(BaseModel):
    ids: Optional[List[int]] = None
    names: Optional[List[str]] = None
    types: Optional[List[WalletType]] = None

    initial_balance_min: Optional[Decimal] = None
    initial_balance_max: Optional[Decimal] = None

    balance_min: Optional[Decimal] = None
    balance_max: Optional[Decimal] = None

    created_at_from: Optional[datetime] = None
    created_at_to: Optional[datetime] = None

    updated_at_from: Optional[datetime] = None
    updated_at_to: Optional[datetime] = None

    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=1000)

    with_stats: bool = False
    stats_date_from: Optional[datetime] = None
    stats_date_to: Optional[datetime] = None