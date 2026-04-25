from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .schemas import (
    WalletRead,
    WalletCreate,
    WalletUpdate,
    WalletFilters,
)
from .service import service
from app.db.postgres.session import get_db


wallets_router = APIRouter(prefix="/wallets", tags=["wallets"])


# --- READ OPERATIONS ---
@wallets_router.get("/", response_model=List[WalletRead])
async def get_wallets(
    filters: WalletFilters = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_wallets(db, filters)


@wallets_router.get("/{wallet_id}", response_model=WalletRead)
async def get_wallet(
    wallet_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_wallet(db, wallet_id)


# --- CREATE OPERATIONS ---
@wallets_router.post("/", response_model=WalletRead, status_code=status.HTTP_201_CREATED)
async def create_wallet(
    data: WalletCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_wallet(db, data)


# --- UPDATE OPERATIONS ---
@wallets_router.patch("/{wallet_id}", response_model=WalletRead)
async def update_wallet(
    wallet_id: int = Path(..., ge=1),
    data: WalletUpdate = ...,
    db: AsyncSession = Depends(get_db)
):
    return await service.update_wallet(db, wallet_id, data)


# --- DELETE OPERATIONS ---
@wallets_router.delete("/{wallet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wallet(
    wallet_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_wallet(db, wallet_id)
