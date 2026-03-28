# wallets/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import (
    Wallet,
    WalletCreate,
    WalletUpdate,
    WalletFilters
)
from .service import service
from app.db.session import get_db  # dependency

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.get("/", response_model=List[Wallet])
async def get_wallets(
    filters: WalletFilters = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_wallets(db, filters)


@router.get("/{wallet_id}", response_model=Wallet)
async def get_wallet(
    wallet_id: int,
    db: AsyncSession = Depends(get_db)
):
    wallet = await service.get_wallet(db, wallet_id)

    if not wallet:
        raise HTTPException(404, "Wallet not found")

    return wallet


@router.post("/", response_model=Wallet, status_code=201)
async def create_wallet(
    data: WalletCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_wallet(db, data)


@router.patch("/{wallet_id}", response_model=Wallet)
async def update_wallet(
    wallet_id: int,
    data: WalletUpdate,
    db: AsyncSession = Depends(get_db)
):
    wallet = await service.update_wallet(db, wallet_id, data)

    if not wallet:
        raise HTTPException(404, "Wallet not found")

    return wallet


@router.delete("/{wallet_id}", status_code=204)
async def delete_wallet(
    wallet_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted = await service.delete_wallet(db, wallet_id)

    if not deleted:
        raise HTTPException(404, "Wallet not found")