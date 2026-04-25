from typing import List, Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Wallet
from .schemas import WalletFilters


class WalletRepository:

    # READ OPERATIONS
    async def get_one_by_id(
        self, db: AsyncSession, wallet_id: int
    ) -> Optional[Wallet]:
        result = await db.execute(
            select(Wallet).where(Wallet.id == wallet_id)
        )
        return result.scalar_one_or_none()

    async def get_many_by_filters(
        self, db: AsyncSession, filters: WalletFilters
    ) -> List[Wallet]:
        query = select(Wallet)

        # --- filters ---
        if filters.ids:
            if not filters.ids:
                return []
            query = query.where(Wallet.id.in_(filters.ids))

        if filters.names:
            query = query.where(Wallet.name.in_(filters.names))

        if filters.types:
            query = query.where(Wallet.type.in_(filters.types))

        if filters.balance_min is not None:
            query = query.where(Wallet.balance >= filters.balance_min)

        if filters.balance_max is not None:
            query = query.where(Wallet.balance <= filters.balance_max)

        if filters.created_at_from is not None:
            query = query.where(Wallet.created_at >= filters.created_at_from)

        if filters.created_at_to is not None:
            query = query.where(Wallet.created_at <= filters.created_at_to)

        # --- sorting ---
        query = query.order_by(Wallet.id.desc())

        # --- pagination ---
        if filters.skip is not None:
            query = query.offset(filters.skip)

        limit = min(filters.limit or 100, 1000)
        query = query.limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    # CREATE OPERATIONS
    async def create_one(
        self, db: AsyncSession, wallet: dict
    ) -> Optional[Wallet]:
        result = await db.execute(
            insert(Wallet)
            .values(**wallet)
            .on_conflict_do_nothing(index_elements=["name"])
            .returning(Wallet)
        )
        return result.scalar_one_or_none()

    # UPDATE OPERATIONS
    async def update_one(
        self, db: AsyncSession, wallet_id: int, wallet: dict
    ) -> Optional[Wallet]:
        result = await db.execute (
            update(Wallet)
            .where(Wallet.id == wallet_id)
            .values(**wallet)
            .returning(Wallet)
        )
        return result.scalar_one_or_none()

    # DELETE OPERATIONS
    async def delete_one(
        self, db: AsyncSession, wallet_id: int
    ) -> Optional[int]:
        result = await db.execute (
            delete(Wallet)
            .where(Wallet.id == wallet_id)
            .returning(Wallet.id)
        )
        return result.scalar_one_or_none()


repository = WalletRepository()