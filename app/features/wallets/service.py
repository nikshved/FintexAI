# wallets/service.py

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .repo import WalletRepository
from .schemas import WalletCreate, WalletUpdate, WalletFilters


class WalletService:

    def __init__(self):
        self.repo = WalletRepository()

    # ===== GET ONE =====
    async def get_wallet(
        self,
        db: AsyncSession,
        wallet_id: int
    ):
        return await self.repo.get_by_id(db, wallet_id)

    # # ===== GET BULK =====
    # async def get_wallets(
    #     self,
    #     db: AsyncSession,
    #     filters: WalletFilters
    # ):
    #     return await self.repo.get_many(db, filters)

    # # ===== CREATE ONE =====
    # async def create_wallet(
    #     self,
    #     db: AsyncSession,
    #     data: WalletCreate
    # ):
    #     try:
    #         wallet = await self.repo.create(
    #             db,
    #             data.model_dump()
    #         )
    #         await db.commit()
    #         return wallet

    #     except Exception:
    #         await db.rollback()
    #         raise

    # # ===== CREATE BULK =====
    # async def create_wallets(
    #     self,
    #     db: AsyncSession,
    #     data: List[WalletCreate]
    # ):
    #     if not data:
    #         return []

    #     try:
    #         wallets = await self.repo.create_many(
    #             db,
    #             [w.model_dump() for w in data]
    #         )
    #         await db.commit()
    #         return wallets

    #     except Exception:
    #         await db.rollback()
    #         raise

    # # ===== UPDATE =====
    # async def update_wallet(
    #     self,
    #     db: AsyncSession,
    #     wallet_id: int,
    #     data: WalletUpdate
    # ):
    #     wallet = await self.repo.get_by_id(db, wallet_id)

    #     if not wallet:
    #         return None

    #     try:
    #         updated = await self.repo.update(
    #             db,
    #             wallet,
    #             data.model_dump(exclude_unset=True)
    #         )
    #         await db.commit()
    #         return updated

    #     except Exception:
    #         await db.rollback()
    #         raise

    # # ===== DELETE ONE =====
    # async def delete_wallet(
    #     self,
    #     db: AsyncSession,
    #     wallet_id: int
    # ):
    #     wallet = await self.repo.get_by_id(db, wallet_id)

    #     if not wallet:
    #         return False

    #     try:
    #         await self.repo.delete(db, wallet)
    #         await db.commit()
    #         return True

    #     except Exception:
    #         await db.rollback()
    #         raise

    # # ===== DELETE BULK =====
    # async def delete_wallets(
    #     self,
    #     db: AsyncSession,
    #     ids: List[int]
    # ):
    #     if not ids:
    #         return 0

    #     try:
    #         deleted_count = await self.repo.delete_many(db, ids)
    #         await db.commit()
    #         return deleted_count

    #     except Exception:
    #         await db.rollback()
    #         raise


service = WalletService()