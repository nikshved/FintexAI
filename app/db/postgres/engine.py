from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,

    echo=False,          # True только в dev
    pool_size=10,        # размер пула
    max_overflow=20,     # дополнительный пул
    pool_timeout=30,

    pool_recycle=1800,   # переподключение
    pool_pre_ping=True,  # проверка соединения
)