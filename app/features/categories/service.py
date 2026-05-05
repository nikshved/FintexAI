from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional

from app.core.exceptions import ConflictError, NotFoundError, DatabaseError
from .models import Category
from .repo import category_repo

from .schemas import (
    CategoryCreate,
    CategoryUpdate,
    CategoryFilters,
)


class CategoryService:
    def __init__(self):
        self.repo = category_repo

    # --- READ OPERATIONS ---
    async def get_category(self, db: AsyncSession, category_id: int) -> Category:
        try:
            category = await self.repo.get_one_by_id(db, category_id)

            if category is None:
                raise NotFoundError(f"Category with id {category_id} not found")

            return category

        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error")

    async def get_сategories(
        self, db: AsyncSession, filters: CategoryFilters
    ) -> List[Category]:
        try:
            categories = await self.repo.get_many_by_filters(db, filters)

            return categories

        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error")

    # --- CREATE OPERATIONS ---
    async def create_сategory(self, db: AsyncSession, data: CategoryCreate) -> Category:
        try:
            created_сategory = await self.repo.create_one(db, data.model_dump())

            if created_сategory is None:
                raise ConflictError("Category already exists")

            await db.commit()
            return created_сategory

        except IntegrityError:
            await db.rollback()
            orig = str(e.orig).lower()
            if "foreign key" in orig:
                raise NotFoundError(f"Wallet {data.wallet_id} not found")
            raise ConflictError("Category already exists")

        except SQLAlchemyError as e:
            print("SOMETHING WENT WRONG WITH THE DATABASE:", e)
            await db.rollback()
            raise DatabaseError(f"Database error")

    # --- UPDATE OPERATIONS ---
    async def update_сategory(
        self, db: AsyncSession, сategory_id: int, data: CategoryUpdate
    ) -> Optional[Category]:
        try:
            update_data = data.model_dump(exclude_unset=True)

            if not update_data:
                raise ConflictError("No data provided for update")

            updated_сategory = await self.repo.update_one(db, сategory_id, update_data)

            if updated_сategory is None:
                raise NotFoundError(f"Category with id {сategory_id} not found")

            await db.commit()
            return updated_сategory
        except IntegrityError:
            await db.rollback()
            raise ConflictError("Category already exists")

        except SQLAlchemyError as e:
            await db.rollback()
            print("SOMETHING WENT WRONG WITH THE DATABASE:", e)
            raise DatabaseError(f"Database error")

    # --- DELETE OPERATIONS ---
    async def delete_сategory(self, db: AsyncSession, сategory_id: int) -> None:
        try:
            deleted_сategory_id = await self.repo.delete_one(db, сategory_id)

            if deleted_сategory_id is None:
                raise NotFoundError(f"Category with id {сategory_id} not found")

            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            print("SOMETHING WENT WRONG WITH THE DATABASE:", e)
            raise DatabaseError(f"Database error")


category_service = CategoryService()
