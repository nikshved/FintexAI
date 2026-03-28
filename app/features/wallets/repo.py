# wallets/repository.py

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from .models import Wallet
from .schemas import WalletFilters


class WalletRepository:

    async def get_by_id(
        self,
        db: AsyncSession,
        wallet_id: int
    ) -> Optional[Wallet]:
        return await db.get(Wallet, wallet_id)


    async def get_many(
        self,
        db: AsyncSession,
        filters: WalletFilters
    ) -> List[Wallet]:

        query = select(Wallet)

        # 🔥 фильтры
        if filters.ids:
            query = query.where(Wallet.id.in_(filters.ids))

        if filters.types:
            query = query.where(Wallet.type.in_(filters.types))

        if filters.balance_min is not None:
            query = query.where(Wallet.balance >= filters.balance_min)

        if filters.balance_max is not None:
            query = query.where(Wallet.balance <= filters.balance_max)

        # pagination
        query = query.offset(filters.skip).limit(filters.take)

        result = await db.execute(query)
        return result.scalars().all()


    async def create(
        self,
        db: AsyncSession,
        wallet_data: dict
    ) -> Wallet:

        wallet = Wallet(**wallet_data)
        db.add(wallet)
        await db.flush()  # получаем id

        return wallet


    async def create_many(
        self,
        db: AsyncSession,
        wallets_data: List[dict]
    ) -> List[Wallet]:

        wallets = [Wallet(**data) for data in wallets_data]
        db.add_all(wallets)

        await db.flush()
        return wallets


    async def update(
        self,
        db: AsyncSession,
        wallet: Wallet,
        data: dict
    ) -> Wallet:

        for field, value in data.items():
            setattr(wallet, field, value)

        await db.flush()
        return wallet


    async def delete(
        self,
        db: AsyncSession,
        wallet: Wallet
    ):
        await db.delete(wallet)