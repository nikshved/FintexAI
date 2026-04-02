from sqlalchemy import bindparam, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .models import Wallet
from .schemas import WalletFilters


class WalletRepository:

    async def get_one_by_id(self, db: AsyncSession, wallet_id: int) -> Wallet | None:
        query = select(Wallet).where(Wallet.id == wallet_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_many_by_filters(self, db: AsyncSession, filters: WalletFilters) -> List[Wallet]:
        query = select(Wallet)

        if filters.ids:
            query = query.where(Wallet.id.in_(filters.ids))
        if filters.names:
            query = query.where(Wallet.name.in_(filters.names))
        if filters.types:
            query = query.where(Wallet.type.in_(filters.types))
        if filters.initial_balance_min is not None:
            query = query.where(Wallet.initial_balance >= filters.initial_balance_min)
        if filters.initial_balance_max is not None:
            query = query.where(Wallet.initial_balance <= filters.initial_balance_max)
        if filters.balance_min is not None:
            query = query.where(Wallet.balance >= filters.balance_min)
        if filters.balance_max is not None:
            query = query.where(Wallet.balance <= filters.balance_max)
        
        query = query.order_by(Wallet.id.desc())

        if filters.skip:
            query = query.offset(filters.skip)
        
        limit = min(filters.limit or 100, 1000)
        query = query.limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create_one(self, db: AsyncSession, wallet_data: dict) -> Wallet:
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
        if not wallets_data:
            return []
        try:
            query = insert(Wallet).values(wallets_data).returning(Wallet)
            result = await db.execute(query)
            new_wallets = list(result.scalars().all())
            await db.commit()
            return new_wallets
        except Exception:
            await db.rollback()
            raise

    async def update_one(self, db: AsyncSession, wallet_id: int, data: dict) -> Wallet | None: 
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
        if not wallets_data:
            return []
        try:
            # Важно: предполагаем, что ключи во всех словарях одинаковые
            query = (
                update(Wallet)
                .where(Wallet.id == bindparam("id"))
                .values({
                    col: bindparam(col) 
                    for col in wallets_data[0].keys() if col != "id"
                })
                .returning(Wallet)
            )
            result = await db.execute(query, wallets_data)
            updated_wallets = list(result.scalars().all())
            
            if updated_wallets:
                await db.commit()
            return updated_wallets
        except Exception:
            await db.rollback()
            raise

    async def delete_one(self, db: AsyncSession, wallet_id: int) -> bool:
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
        if not wallet_ids:
            return []
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