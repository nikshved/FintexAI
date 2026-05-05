from typing import List, Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Transaction


class TransactionRepository:
    # READ OPERATIONS
    async def get_one_by_id(self, db: AsyncSession, transaction_id: int) -> Optional[Transaction]:
        result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
        return result.scalar_one_or_none()

    async def get_many_by_filters(
        self, db: AsyncSession, query
    ) -> List[Transaction]:
        result = await db.execute(query)
        return list(result.scalars().all())

    # CREATE OPERATIONS
    async def create_one(self, db: AsyncSession, data: dict) -> Optional[Transaction]:
        result = await db.execute(
            insert(Transaction)
            .values(**data)
            .returning(Transaction)
        )
        return result.scalar_one_or_none()
    
    # UPDATE OPERATIONS
    async def update_one(
        self, db: AsyncSession, transaction_id: int, data: dict
    ) -> Optional[Transaction]:
        result = await db.execute(
            update(Transaction)
            .where(Transaction.id == transaction_id)
            .values(**data)
            .returning(Transaction)
        )
        return result.scalar_one_or_none()

    # DELETE OPERATIONS
    async def delete_one(self, db: AsyncSession, transaction_id: int) -> Optional[int]:
        result = await db.execute(
            delete(Transaction)
            .where(Transaction.id == transaction_id)
            .returning(Transaction.id)
        )
        return result.scalar_one_or_none()


repo = TransactionRepository()
