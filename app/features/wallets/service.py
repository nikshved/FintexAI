from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from .models import Wallet
from .repo import WalletRepository
from .schemas import (
    WalletCreate, 
    WalletUpdate, 
    WalletFilters, 
    WalletsUpdateItem,
    WalletsDelete
)

class WalletService:
    def __init__(self):
        self.repo = WalletRepository()
    
    # --- READ OPERATIONS ---

    async def get_wallet(self, db: AsyncSession, wallet_id: int) -> Optional[Wallet]:
        """Fetch a single wallet by its unique ID"""
        return await self.repo.get_one_by_id(db, wallet_id)

    async def get_wallets(self, db: AsyncSession, filters: WalletFilters) -> List[Wallet]:
        """Fetch multiple wallets based on provided filters and pagination"""
        return await self.repo.get_many_by_filters(db, filters)
    
    # --- CREATE OPERATIONS ---

    async def create_wallet(self, db: AsyncSession, data: WalletCreate) -> Wallet:
        """Create a new wallet entry in the database"""
        # updated_at will be handled by the database automatically
        return await self.repo.create_one(db, data.model_dump())

    async def create_wallets(self, db: AsyncSession, data: List[WalletCreate]) -> List[Wallet]:
        """Bulk create multiple wallet entries"""
        wallets_dicts = [item.model_dump() for item in data]
        return await self.repo.create_many(db, wallets_dicts)

    # --- UPDATE OPERATIONS ---

    async def update_wallet(self, db: AsyncSession, wallet_id: int, data: WalletUpdate) -> Optional[Wallet]:
        """
        Update an existing wallet. 
        The 'updated_at' field is automatically refreshed by SQLAlchemy/PostgreSQL.
        """
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return None
        return await self.repo.update_one(db, wallet_id, update_data)

    async def update_wallets(self, db: AsyncSession, data: List[WalletsUpdateItem]) -> List[Wallet]:
        """Bulk update multiple wallets. Database handles individual 'updated_at' timestamps."""
        # Ensure we keep the ID for the repository to identify the rows
        update_list = [item.model_dump(exclude_unset=True) for item in data]
        return await self.repo.update_many(db, update_list)

    # --- DELETE OPERATIONS ---

    async def delete_wallet(self, db: AsyncSession, wallet_id: int) -> bool:
        """Remove a single wallet from the database"""
        return await self.repo.delete_one(db, wallet_id)

    async def delete_wallets(self, db: AsyncSession, data: WalletsDelete) -> Dict[str, Any]:
        """Bulk delete wallets and return the result summary"""
        deleted_ids = await self.repo.delete_many(db, data.ids)
        
        return {
            "deleted_ids": deleted_ids,
            "count": len(deleted_ids)
        }

# Global service instance
service = WalletService()