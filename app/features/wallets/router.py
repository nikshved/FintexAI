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
    WalletsDelete,
)
from .service import service
from app.db.postgres.session import get_db


wallets_router = APIRouter(prefix="/wallets", tags=["wallets"])

# --- READ OPERATIONS ---


@wallets_router.get(
    "/", response_model=List[WalletRead], status_code=status.HTTP_200_OK
)
async def get_wallets(
    filters: WalletFilters = Depends(), db: AsyncSession = Depends(get_db)
):
    return await service.get_wallets(db, filters)


@wallets_router.get("/{wallet_id}", response_model=WalletRead)
async def get_wallet(wallet_id: int, db: AsyncSession = Depends(get_db)):
    wallet = await service.get_wallet(db, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


# --- CREATE OPERATIONS ---


@wallets_router.post(
    "/", response_model=WalletRead, status_code=status.HTTP_201_CREATED
)
async def create_wallet(data: WalletCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_wallet(db, data)


@wallets_router.post(
    "/bulk", response_model=List[WalletRead], status_code=status.HTTP_201_CREATED
)
async def create_wallets(data: WalletsCreate, db: AsyncSession = Depends(get_db)):
    """Create multiple wallets in one request"""
    return await service.create_wallets(db, data.wallets)


# --- UPDATE OPERATIONS ---


@wallets_router.patch("/{wallet_id}", response_model=WalletRead)
async def update_wallet(
    wallet_id: int, data: WalletUpdate, db: AsyncSession = Depends(get_db)
):
    wallet = await service.update_wallet(db, wallet_id, data)

    if not wallet:
        raise HTTPException(
            status_code=404, detail="Wallet not found or no data to update"
        )
    return wallet


@wallets_router.patch("/bulk", response_model=List[WalletRead])
async def bulk_update_wallets(data: WalletsUpdate, db: AsyncSession = Depends(get_db)):
    return await service.update_wallets(db, data.wallets)


# --- DELETE OPERATIONS ---


@wallets_router.delete("/{wallet_id}")
async def delete_wallet(wallet_id: int, db: AsyncSession = Depends(get_db)):
    success = await service.delete_wallet(db, wallet_id)

    if not success:
        raise HTTPException(
            status_code=404, detail=f"Wallet with ID {wallet_id} not found"
        )

    return {
        "status": "success",
        "message": "Wallet deleted successfully",
        "wallet_id": wallet_id,
    }


@wallets_router.delete("/", status_code=status.HTTP_200_OK)
async def delete_wallets(data: WalletsDelete, db: AsyncSession = Depends(get_db)):
    return await service.delete_wallets(db, data)
