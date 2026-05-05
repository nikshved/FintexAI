from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .schemas import (
    CategoryRead,
    CategoryCreate,
    CategoryUpdate,
    CategoryFilters,
)
from .service import category_service
from app.db.postgres.session import get_db


categories_router = APIRouter(prefix="/categories", tags=["categories"])


# --- READ OPERATIONS ---
@categories_router.get("/", response_model=List[CategoryRead])
async def get_categories(
    filters: CategoryFilters = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await category_service.get_сategories(db, filters)


@categories_router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)
):
    return await category_service.get_category(db, category_id)


# --- CREATE OPERATIONS ---
@categories_router.post(
    "/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED
)
async def create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await category_service.create_category(db, data)


# --- UPDATE OPERATIONS ---
@categories_router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int = Path(..., ge=1),
    data: CategoryUpdate = ...,
    db: AsyncSession = Depends(get_db),
):
    return await category_service.update_category(db, category_id, data)


# --- DELETE OPERATIONS ---
@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)
):
    return await category_service.delete_category(db, category_id)
