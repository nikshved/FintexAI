from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum


class WalletType(str, Enum):
    SAVINGS = "SAVINGS"
    SPENDINGS = "SPENDINGS"


class Wallet(BaseModel):
    id: int
    name: str
    type: WalletType
    balance: float
    init_balance: float
    init_date: datetime


class WalletCreate(BaseModel):
    name: str = Field(min_length=1)
    type: WalletType
    balance: float = 0
    init_balance: float = 0
    init_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WalletUpdate(BaseModel):
    id: int = Field(gt=0)
    name: Optional[str] = None
    type: Optional[WalletType] = None
    balance: Optional[float] = None
    init_balance: Optional[float] = None


class WalletFilters(BaseModel):
    ids: Optional[List[int]] = None
    names: Optional[List[str]] = None
    types: Optional[List[WalletType]] = None

    init_balance_min: Optional[float] = None
    init_balance_max: Optional[float] = None

    balance_min: Optional[float] = None
    balance_max: Optional[float] = None

    init_date_from: Optional[datetime] = None
    init_date_to: Optional[datetime] = None

    category_ids: Optional[List[int]] = None

    skip: int = 0
    take: int = 50

    with_stats: bool = False
    stats_date_from: Optional[datetime] = None
    stats_date_to: Optional[datetime] = None


class WalletsDelete(BaseModel):
    ids: List[int]


class WalletsCreate(BaseModel):
    wallets: List[WalletCreate]


class WalletsUpdate(BaseModel):
    wallets: List[WalletUpdate]