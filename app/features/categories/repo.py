from typing import List, Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Category
from .schemas import CategoryFilters


class CategoryRepository:
    # READ OPERATIONS
    async def get_one_by_id(self, db: AsyncSession, category_id: int) -> Optional[Category]:
        result = await db.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    async def get_many_by_filters(
        self, db: AsyncSession, filters: CategoryFilters
    ) -> List[Category]:
        query = select(Category)

        # --- filters ---
        if filters.ids:
            if not filters.ids:
                return []
            query = query.where(Category.id.in_(filters.ids))

        if filters.names:
            query = query.where(Category.name.in_(filters.names))
        
        if filters.current_budget_limit is not None:
            query = query.where(Category.current_budget_limit == filters.current_budget_limit)  

        if filters.current_budget_limit_min is not None:
            query = query.where(Category.current_budget_limit >= filters.current_budget_limit_min)

        if filters.current_budget_limit_max is not None:
            query = query.where(Category.current_budget_limit <= filters.current_budget_limit_max)  
        
        if filters.created_at is not None:
            query = query.where(Category.created_at == filters.created_at)

        if filters.created_at_from is not None:
            query = query.where(Category.created_at >= filters.created_at_from)

        if filters.created_at_to is not None:
            query = query.where(Category.created_at <= filters.created_at_to)

        # --- sorting ---
        query = query.order_by(Category.id.desc())

        # --- pagination ---
        if filters.skip is not None:
            query = query.offset(filters.skip)

        limit = min(filters.limit or 100, 1000)
        query = query.limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    # CREATE OPERATIONS
    async def create_one(self, db: AsyncSession, data: dict) -> Optional[Category]:
        result = await db.execute(
            insert(Category)
            .values(**data)
            .returning(Category)
        )
        return result.scalar_one_or_none()

    # UPDATE OPERATIONS
    async def update_one(
        self, db: AsyncSession, category_id: int, data: dict
    ) -> Optional[Category]:
        result = await db.execute(
            update(Category)
            .where(Category.id == category_id)
            .values(**data)
            .returning(Category)
        )
        return result.scalar_one_or_none()

    # DELETE OPERATIONS
    async def delete_one(self, db: AsyncSession, category_id: int) -> Optional[int]:
        result = await db.execute(
            delete(Category).where(Category.id == category_id).returning(Category.id)
        )
        return result.scalar_one_or_none()


repository = CategoryRepository()
