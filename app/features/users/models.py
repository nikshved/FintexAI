from sqlalchemy import String, Boolean, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

from backend.app.db.postgres.base import Base


class User(Base):
    """
    ORM модель пользователя.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True
    )  # admin or system bun user or
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)  # verifed or not

    # # Связь с ролями
    # roles = relationship(
    #     "Role",
    #     secondary="user_roles",
    #     back_populates="users",
    #     lazy="selectin"
    # )
