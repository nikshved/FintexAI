import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

# Твои импорты
from app.core.config import settings
from app.db.postgres.base import Base

# Важно: централизованный импорт всех моделей для работы autogenerate
import app.db.imports

# Объект конфигурации Alembic
config = context.config

# Настройка логирования на основе файла alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Динамически подставляем URL из настроек приложения
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Метаданные моделей
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме (генерация SQL-скриптов)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Позволяет Alembic видеть изменение длины или типа колонок
        compare_type=True,
        # Позволяет видеть изменения дефолтных значений на уровне БД
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Синхронный запуск миграций внутри асинхронного соединения."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        # Полезно, если планируешь использовать несколько схем в Postgres
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме (асинхронное подключение)."""

    # Создаем асинхронный движок
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Поскольку Alembic синхронный внутри, используем run_sync
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# Входная точка
if context.is_offline_mode():
    run_migrations_offline()
else:
    # Стандартный запуск для современных Python скриптов
    asyncio.run(run_migrations_online())
