from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from .models import Wallet
from .schemas import WalletFilters


class WalletRepository:
    """Repository for handling low-level database operations for Wallets"""

    # --- READ OPERATIONS ---

    async def get_one_by_id(self, db: AsyncSession, wallet_id: int) -> Optional[Wallet]:
        """Fetch a single wallet by its primary key"""
        query = select(Wallet).where(Wallet.id == wallet_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_many_by_filters(self, db: AsyncSession, filters: WalletFilters) -> List[Wallet]:
        """Fetch wallets based on dynamic filtering and pagination"""
        query = select(Wallet)

        # Apply filters
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
        
        # Default ordering
        query = query.order_by(Wallet.id.desc())

        # Pagination
        if filters.skip:
            query = query.offset(filters.skip)
        
        limit = min(filters.limit or 100, 1000)
        query = query.limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())

    # --- CREATE OPERATIONS ---

    async def create_one(self, db: AsyncSession, wallet_data: dict) -> Wallet:
        """Insert a single wallet and return the new record"""
        try:
            query = insert(Wallet).values(**wallet_data).returning(Wallet)
            result = await db.execute(query)
            new_wallet = result.scalar_one()
            await db.commit()
            return new_wallet
        except Exception:
            await db.rollback()
            raise

    async def create_many(self, db: AsyncSession, wallets_data: List[dict]) -> List[Wallet]:
        """Insert multiple wallets in a single transaction"""
        try:
            query = insert(Wallet).values(wallets_data).returning(Wallet)
            result = await db.execute(query)
            new_wallets = list(result.scalars().all())
            await db.commit()
            return new_wallets
        except Exception:
            await db.rollback()
            raise

    # --- UPDATE OPERATIONS ---

    async def update_one(self, db: AsyncSession, wallet_id: int, data: dict) -> Optional[Wallet]: 
        """Update a specific wallet and return the updated record"""
        try:
            query = (
                update(Wallet)
                .where(Wallet.id == wallet_id)
                .values(**data)
                .returning(Wallet)
            )
            result = await db.execute(query)
            updated_wallet = result.scalar_one_or_none()
            
            if updated_wallet:
                await db.commit()
            return updated_wallet
        except Exception:
            await db.rollback()
            raise

    async def update_many(self, db: AsyncSession, wallets_data: List[dict]) -> List[Wallet]:
        """Update multiple wallets individually within a single transaction"""
        updated_wallets = []
        try:
            for data in wallets_data:
                # Extract ID and only proceed if present
                wallet_id = data.pop("id", None)
                if wallet_id is None:
                    continue

                query = (
                    update(Wallet)
                    .where(Wallet.id == wallet_id)
                    .values(**data) 
                    .returning(Wallet)
                )
                
                result = await db.execute(query)
                updated_obj = result.scalar_one_or_none()
                
                if updated_obj:
                    updated_wallets.append(updated_obj)

            if updated_wallets:
                await db.commit()
                
            return updated_wallets
        except Exception:
            await db.rollback()
            raise
            
    # --- DELETE OPERATIONS ---

    async def delete_one(self, db: AsyncSession, wallet_id: int) -> bool:
        """Delete a wallet by ID and return success status"""
        try:
            query = delete(Wallet).where(Wallet.id == wallet_id).returning(Wallet.id)
            result = await db.execute(query)
            deleted_id = result.scalar_one_or_none()
            
            if deleted_id:
                await db.commit()
                return True
            return False
        except Exception:
            await db.rollback()
            raise
    
    async def delete_many(self, db: AsyncSession, wallet_ids: List[int]) -> List[int]:
        """Delete multiple wallets and return list of deleted IDs"""
        try:
            query = delete(Wallet).where(Wallet.id.in_(wallet_ids)).returning(Wallet.id)
            result = await db.execute(query)
            deleted_ids = list(result.scalars().all())
            
            if deleted_ids:
                await db.commit()
            return deleted_ids
        except Exception:
            await db.rollback()
            raise