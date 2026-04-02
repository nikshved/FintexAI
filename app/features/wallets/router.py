from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .schemas import (
    WalletRead,
    WalletCreate,
    WalletUpdate,
    WalletFilters,
    WalletsCreate,
    WalletsUpdate,
    WalletsDelete
)
from .service import service
from app.db.postgres.session import get_db


wallets_router = APIRouter(prefix="/wallets", tags=["wallets"])


# ===== GET SINGLE =====
@wallets_router.get("/{wallet_id}", response_model=WalletRead)
async def get_wallet(
    wallet_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_wallet(db, wallet_id)


# ===== CREATE SINGLE =====
@wallets_router.post("/", response_model=WalletRead, status_code=status.HTTP_201_CREATED)
async def create_wallet(
    data: WalletCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_wallet(db, data)


# ===== UPDATE =====
@wallets_router.patch("/{wallet_id}", response_model=WalletRead)
async def update_wallet(
    wallet_id: int,
    data: WalletUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await service.update_wallet(db, wallet_id, data)


# ===== DELETE  SINGLE =====
@wallets_router.delete("/{wallet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wallet(
    wallet_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_wallet(db, wallet_id)


# **************** BULK ACTIONS ****************


# ===== GET BULK =====
@wallets_router.get("/", response_model=List[WalletRead], status_code=status.HTTP_200_OK)
async def get_wallets(
    filters: WalletFilters = Depends(), # Query srtring
    db: AsyncSession = Depends(get_db)
):
    return await service.get_wallets(db, filters)


# ===== CREATE BULK =====
@wallets_router.post("/", response_model=List[WalletRead], status_code=status.HTTP_201_CREATED)
async def create_wallets(
    data: WalletsCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_wallets(db, data.wallets)


# ===== UPDATE BULK =====
@wallets_router.patch("/", response_model=List[WalletRead], status_code=status.HTTP_200_OK)
async def bulk_update_wallets(
    data: WalletsUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await service.update_wallets(db, data.wallets)


# ===== DELETE BULK =====
@wallets_router.delete("/", status_code=status.HTTP_200_OK)
async def delete_wallets(
    data: WalletsDelete,
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_wallets(db, data)


