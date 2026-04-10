from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from .models import Wallet
from .schemas import WalletFilters


class WalletRepository:
    # --- READ OPERATIONS ---

    async def get_one_by_id(self, db: AsyncSession, wallet_id: int) -> Optional[Wallet]:
        query = select(Wallet).where(Wallet.id == wallet_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_many_by_filters(
        self, db: AsyncSession, filters: WalletFilters
    ) -> List[Wallet]:
        query = select(Wallet)

        if filters.ids:
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

        query = query.order_by(Wallet.id.desc())

        if filters.skip is not None:
            query = query.offset(filters.skip)

        query = query.limit(filters.limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    # --- CREATE OPERATIONS ---

    async def create_one(self, db: AsyncSession, wallet_data: dict) -> Wallet:
        query = insert(Wallet).values(**wallet_data).returning(Wallet)
        result = await db.execute(query)
        return result.scalar_one()

    async def create_many(
        self, db: AsyncSession, wallets_data: List[dict]
    ) -> List[Wallet]:
        query = insert(Wallet).values(wallets_data).returning(Wallet)
        result = await db.execute(query)
        return list(result.scalars().all())

    # --- UPDATE OPERATIONS ---

    async def update_one(
        self, db: AsyncSession, wallet_id: int, data: dict
    ) -> Optional[Wallet]:
        query = (
            update(Wallet)
            .where(Wallet.id == wallet_id)
            .values(**data)
            .returning(Wallet)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def update_many(
        self, db: AsyncSession, wallets_data: List[dict]
    ) -> List[Wallet]:
        if not wallets_data:
            return []

        valid_data = [
            d for d in wallets_data
            if d.get("id") and len({k: v for k, v in d.items() if k != "id"}) > 0
        ]

        if not valid_data:
            return []

        await db.execute(update(Wallet), valid_data)

        ids = [d["id"] for d in valid_data]
        result = await db.execute(select(Wallet).where(Wallet.id.in_(ids)))
        return list(result.scalars().all())

    # --- DELETE OPERATIONS ---

    async def delete_one(self, db: AsyncSession, wallet_id: int) -> bool:
        query = delete(Wallet).where(Wallet.id == wallet_id).returning(Wallet.id)
        result = await db.execute(query)
        deleted_id = result.scalar_one_or_none()
        return deleted_id is not None

    async def delete_many(self, db: AsyncSession, wallet_ids: List[int]) -> List[int]:
        query = delete(Wallet).where(Wallet.id.in_(wallet_ids)).returning(Wallet.id)
        result = await db.execute(query)
        return list(result.scalars().all())


repository = WalletRepository()