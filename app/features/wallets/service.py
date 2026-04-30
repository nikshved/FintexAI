from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional

from app.core.exceptions import ConflictError, NotFoundError, DatabaseError
from .models import Wallet
from .repo import WalletRepository

from .schemas import (
    WalletCreate,
    WalletUpdate,
    WalletFilters,
)


class WalletService:
    def __init__(self):
        self.repo = WalletRepository()

    # --- READ OPERATIONS ---
    async def get_wallet(self, db: AsyncSession, wallet_id: int) -> Wallet:
        try:
            wallet = await self.repo.get_one_by_id(db, wallet_id)

            if wallet is None:
                raise NotFoundError(f"Wallet with id {wallet_id} not found")

            return wallet

        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error")

    async def get_wallets(
        self, db: AsyncSession, filters: WalletFilters
    ) -> List[Wallet]:
        try:
            wallets = await self.repo.get_many_by_filters(db, filters)

            return wallets

        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error")

    # --- CREATE OPERATIONS ---
    async def create_wallet(self, db: AsyncSession, data: WalletCreate) -> Wallet:
        try:
            created_wallet = await self.repo.create_one(db, data.model_dump())

            if created_wallet is None:
                raise ConflictError("Wallet already exists")

            await db.commit()
            return created_wallet

        except IntegrityError:
            await db.rollback()
            raise ConflictError("Wallet already exists")

        except SQLAlchemyError as e:
            print("SOMETHING WENT WRONG WITH THE DATABASE:", e)
            await db.rollback()
            raise DatabaseError(f"Database error")

    # --- UPDATE OPERATIONS ---
    async def update_wallet(
        self, db: AsyncSession, wallet_id: int, data: WalletUpdate
    ) -> Optional[Wallet]:
        try:
            update_data = data.model_dump(exclude_unset=True)

            if not update_data:
                raise ConflictError("No data provided for update")

            updated_wallet = await self.repo.update_one(db, wallet_id, update_data)

            if updated_wallet is None:
                raise NotFoundError(f"Wallet with id {wallet_id} not found")

            await db.commit()
            return updated_wallet
        except IntegrityError:
            await db.rollback()
            raise ConflictError("Wallet already exists")

        except SQLAlchemyError as e:
            await db.rollback()
            print("SOMETHING WENT WRONG WITH THE DATABASE:", e)
            raise DatabaseError(f"Database error")

    # --- DELETE OPERATIONS ---
    async def delete_wallet(self, db: AsyncSession, wallet_id: int) -> None:
        try:
            deleted_wallet_id = await self.repo.delete_one(db, wallet_id)

            if deleted_wallet_id is None:
                raise NotFoundError(f"Wallet with id {wallet_id} not found")

            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            print("SOMETHING WENT WRONG WITH THE DATABASE:", e)
            raise DatabaseError(f"Database error")


service = WalletService()
