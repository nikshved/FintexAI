from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import  IntegrityError, SQLAlchemyError
from typing import List, Optional

from app.core.exceptions import ConflictError, InternalServerError, NotFoundError, DatabaseError
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
            async with db.begin():
                created_wallet = await self.repo.create_one(db, data.name)
                
                if created_wallet is not None:
                    raise ConflictError("Wallet already exists")
                
                return created_wallet
        
        except IntegrityError:
            raise ConflictError("Wallet already exists")
    
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error")


    # --- UPDATE OPERATIONS ---
    async def update_wallet(
        self, db: AsyncSession, wallet_id: int, data: WalletUpdate
    ) -> Optional[Wallet]:
        try:
            update_data = data.model_dump(exclude_unset=True)
            
            if not update_data:
                raise NotFoundError("No data provided for update")
            
            async with db.begin():
                updated_wallet = await self.repo.update_one(db, wallet_id, update_data)
                
                if updated_wallet is None:
                    raise NotFoundError(f"Wallet with id {wallet_id} not found")
                                
                return updated_wallet
        except IntegrityError:
            raise ConflictError("Wallet already exists")
        
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error")


    # --- DELETE OPERATIONS ---
    async def delete_wallet(self, db: AsyncSession, wallet_id: int) -> bool:
        deleted = await self.repo.delete_one(db, wallet_id)
        if deleted:
            await db.commit()
        return deleted

service = WalletService()