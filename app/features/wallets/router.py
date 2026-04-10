from fastapi import APIRouter, Depends, HTTPException, Path, status, Response
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
@wallets_router.get("/", response_model=List[WalletRead])
async def get_wallets(
    filters: WalletFilters = Depends(), db: AsyncSession = Depends(get_db)
):
    return await service.get_wallets(db, filters)


@wallets_router.get("/{wallet_id}", response_model=WalletRead)
async def get_wallet(
    wallet_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)
):
    wallet = await service.get_wallet(db, wallet_id)
    if not wallet:
        raise HTTPException(
            status_code=404, detail=f"Wallet with ID {wallet_id} not found"
        )
    return wallet


# --- CREATE OPERATIONS ---
@wallets_router.post("/", response_model=WalletRead, status_code=status.HTTP_201_CREATED)
async def create_wallet(data: WalletCreate, db: AsyncSession = Depends(get_db)):
    created_wallet = await service.create_wallet(db, data)
    if not created_wallet:
        raise HTTPException(status_code=400, detail="Failed to create wallet")
    return created_wallet


@wallets_router.post("/bulk", response_model=List[WalletRead], status_code=status.HTTP_201_CREATED)
async def create_wallets(
    data: WalletsCreate, response: Response, db: AsyncSession = Depends(get_db)
):
    created_wallets = await service.create_wallets(db, data.wallets)

    if not created_wallets:
        raise HTTPException(status_code=400, detail="No wallets were created")

    if len(created_wallets) < len(data.wallets):
        response.status_code = status.HTTP_207_MULTI_STATUS
    else:
        response.status_code = status.HTTP_201_CREATED

    return created_wallets


# --- UPDATE OPERATIONS ---
@wallets_router.patch("/bulk", response_model=List[WalletRead])
async def bulk_update_wallets(
    data: WalletsUpdate, response: Response, db: AsyncSession = Depends(get_db)
):
    updated_wallets = await service.update_wallets(db, data.wallets)

    if not updated_wallets:
        raise HTTPException(status_code=400, detail="No wallets were updated")

    if len(updated_wallets) < len(data.wallets):
        response.status_code = status.HTTP_207_MULTI_STATUS
    else:
        response.status_code = status.HTTP_200_OK

    return updated_wallets


@wallets_router.patch("/{wallet_id}", response_model=WalletRead)
async def update_wallet(
    wallet_id: int = Path(..., ge=1), data: WalletUpdate = ..., db: AsyncSession = Depends(get_db)
):
    wallet = await service.update_wallet(db, wallet_id, data)
    if not wallet:
        raise HTTPException(
            status_code=404, detail=f"Wallet {wallet_id} not found or no data provided"
        )
    return wallet


# --- DELETE OPERATIONS ---
@wallets_router.delete("/bulk", response_model=List[int])
async def delete_wallets(
    data: WalletsDelete, response: Response, db: AsyncSession = Depends(get_db)
):
    deleted_ids = await service.delete_wallets(db, data.ids)

    if not deleted_ids:
        raise HTTPException(status_code=404, detail="No wallets found for deletion")

    if len(deleted_ids) < len(data.ids):
        response.status_code = status.HTTP_207_MULTI_STATUS
    else:
        response.status_code = status.HTTP_200_OK

    return deleted_ids


@wallets_router.delete("/{wallet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wallet(
    wallet_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)
):
    deleted = await service.delete_wallet(db, wallet_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Wallet {wallet_id} not found")
    return None