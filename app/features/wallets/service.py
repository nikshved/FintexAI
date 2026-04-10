from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .models import Wallet
from .repo import WalletRepository
from .schemas import (
    WalletCreate,
    WalletUpdate,
    WalletFilters,
    WalletsUpdateItem,
)


class WalletService:
    def __init__(self):
        self.repo = WalletRepository()

    # --- READ OPERATIONS ---
    async def get_wallet(self, db: AsyncSession, wallet_id: int) -> Optional[Wallet]:
        return await self.repo.get_one_by_id(db, wallet_id)

    async def get_wallets(
        self, db: AsyncSession, filters: WalletFilters
    ) -> List[Wallet]:
        return await self.repo.get_many_by_filters(db, filters)

    # --- CREATE OPERATIONS ---
    async def create_wallet(self, db: AsyncSession, data: WalletCreate) -> Wallet:
        wallet = await self.repo.create_one(db, data.model_dump())
        await db.commit()
        return wallet

    async def create_wallets(
        self, db: AsyncSession, data: List[WalletCreate]
    ) -> List[Wallet]:
        wallets_dicts = [item.model_dump() for item in data]
        wallets = await self.repo.create_many(db, wallets_dicts)
        await db.commit()
        return wallets

    # --- UPDATE OPERATIONS ---
    async def update_wallet(
        self, db: AsyncSession, wallet_id: int, data: WalletUpdate
    ) -> Optional[Wallet]:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return None
        wallet = await self.repo.update_one(db, wallet_id, update_data)
        if wallet:
            await db.commit()
        return wallet

    async def update_wallets(
        self, db: AsyncSession, data: List[WalletsUpdateItem]
    ) -> List[Wallet]:
        update_list = [
            {"id": item.id, **item.model_dump(exclude_unset=True, exclude={"id"})}
            for item in data
        ]
        wallets = await self.repo.update_many(db, update_list)
        if wallets:
            await db.commit()
        return wallets

    # --- DELETE OPERATIONS ---
    async def delete_wallet(self, db: AsyncSession, wallet_id: int) -> bool:
        deleted = await self.repo.delete_one(db, wallet_id)
        if deleted:
            await db.commit()
        return deleted

    async def delete_wallets(self, db: AsyncSession, ids: List[int]) -> List[int]:
        deleted_ids = await self.repo.delete_many(db, ids)
        if deleted_ids:
            await db.commit()
        return deleted_ids


service = WalletService()