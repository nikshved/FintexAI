from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union

from .schemas import (
    TransactionRead,
    TransactionCreate,
    TransactionUpdate,
    TransactionFilters,
    TransferCreate,
)
from .service import service
from app.db.postgres.session import get_db


transactions_router = APIRouter(prefix="/transactions", tags=["transactions"])


# --- READ OPERATIONS ---
@transactions_router.get("/", response_model=List[TransactionRead])
async def get_transactions(
    filters: TransactionFilters = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_transactions(db, filters)


@transactions_router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(
    transaction_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_transaction(db, transaction_id)


# --- CREATE OPERATIONS ---
@transactions_router.post(
    "/",
    response_model=Union[TransactionRead, List[TransactionRead]],
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    data: Union[TransactionCreate, TransferCreate],
    db: AsyncSession = Depends(get_db),
):
    return await service.create(db, data)


# --- UPDATE OPERATIONS ---
@transactions_router.patch("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: int = Path(..., ge=1),
    data: TransactionUpdate = ...,
    db: AsyncSession = Depends(get_db),
):
    return await service.update_transaction(db, transaction_id, data)


# --- DELETE OPERATIONS ---
@transactions_router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_transaction(
    transaction_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
):
    return await service.delete_transaction(db, transaction_id)