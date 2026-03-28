# wallets/service.py

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .repo import WalletRepository
from .schemas import (
    WalletCreate,
    WalletUpdate,
    WalletFilters
)

repo = WalletRepository()


class WalletService:

    async def get_wallet(
        self,
        db: AsyncSession,
        wallet_id: int
    ):
        return await repo.get_by_id(db, wallet_id)


    async def get_wallets(
        self,
        db: AsyncSession,
        filters: WalletFilters
    ):
        return await repo.get_many(db, filters)


    async def create_wallet(
        self,
        db: AsyncSession,
        data: WalletCreate
    ):
        wallet = await repo.create(
            db,
            data.model_dump()
        )

        await db.commit()
        return wallet


    async def create_wallets(
        self,
        db: AsyncSession,
        data: List[WalletCreate]
    ):
        wallets = await repo.create_many(
            db,
            [w.model_dump() for w in data]
        )

        await db.commit()
        return wallets


    async def update_wallet(
        self,
        db: AsyncSession,
        wallet_id: int,
        data: WalletUpdate
    ):
        wallet = await repo.get_by_id(db, wallet_id)

        if not wallet:
            return None

        updated = await repo.update(
            db,
            wallet,
            data.model_dump(exclude_unset=True)
        )

        await db.commit()
        return updated


    async def delete_wallet(
        self,
        db: AsyncSession,
        wallet_id: int
    ):
        wallet = await repo.get_by_id(db, wallet_id)

        if not wallet:
            return False

        await repo.delete(db, wallet)
        await db.commit()
        return True


service = WalletService()