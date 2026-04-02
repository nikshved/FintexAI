# wallets/repository.py

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from .models import Wallet
from .schemas import WalletFilters


class WalletRepository:

    async def get_one_by_id(
        self,
        db: AsyncSession,
        wallet_id: int
    ) -> Wallet | None:
        query = select(Wallet).where(Wallet.id == wallet_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_many_by_filters(
        self,
        db: AsyncSession,
        filters: WalletFilters
    ) -> List[Wallet]:

        query = select(Wallet)

        # filters
        if filters.ids:
            query = query.where(Wallet.id.in_(filters.ids))
            
        if filters.names:
            query = query.where(Wallet.name.in_(filters.names))

        if filters.types:
            query = query.where(Wallet.type.in_(filters.types))
            
        if filters.initial_balance_min is not None:
            query = query.where(Wallet.init_balance >= filters.initial_balance_min)

        if filters.initial_balance_max is not None:
            query = query.where(Wallet.init_balance <= filters.initial_balance_max)

        if filters.balance_min is not None:
            query = query.where(Wallet.balance >= filters.balance_min)

        if filters.balance_max is not None:
            query = query.where(Wallet.balance <= filters.balance_max)
        
        # sort
        query = query.order_by(Wallet.id.desc())

        # pagination
        if filters.skip:
            query = query.offset(filters.skip)
        
        limit = min(filters.limit or 100, 1000)
        query = query.limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())


    async def create_one(
        self,
        db: AsyncSession,
        wallet_data: dict
    ) -> Wallet:

        wallet = Wallet(**wallet_data)
        db.add(wallet)
        await db.flush()  # get id
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


    async def update_one(
        self,
        db: AsyncSession,
        wallet_id: int,
        data: dict
    ) -> Wallet: 
        query = (
            update(Wallet)
            .where(Wallet.id == wallet_id)
            .values(**data)
            .returning(Wallet)
        )
        result = await db.execute(query)
        await db.commit()
        return result.scalar_one()


    async def delete(
        self,
        db: AsyncSession,
        wallet: Wallet
    ):
        await db.delete(wallet)