from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
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
        try:
            wallet = await self.repo.get_one_by_id(db, wallet_id)
            return  {
                "status": "success",
                "message": "Wallet found",
                "data": wallet
            }
        
        except SQLAlchemyError as e:
            return  {
                "status": "error",
                "message": f"Database error: {e}",
                "data": None
            }
        except Exception as e:
            return  {
                "status": "error",
                "message": f"Unexpected error: {e}",
                "data": None
            }

    async def get_wallets(
        self, db: AsyncSession, filters: WalletFilters
    ) -> List[Wallet]:
        return await self.repo.get_many_by_filters(db, filters)

    # --- CREATE OPERATIONS ---
    async def create_wallet(self, db: AsyncSession, data: WalletCreate) -> Wallet:
        
        wallet = await self.repo.create_one(db, data.model_dump())
        await db.commit()
        return wallet

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

    # --- DELETE OPERATIONS ---
    async def delete_wallet(self, db: AsyncSession, wallet_id: int) -> bool:
        deleted = await self.repo.delete_one(db, wallet_id)
        if deleted:
            await db.commit()
        return deleted

service = WalletService()