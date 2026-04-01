from contextlib import asynccontextmanager
from fastapi import FastAPI

from ..db.postgres.engine import engine
from ..db.postgres.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):

    # STARTUP
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("DB connected")

    yield

    # SHUTDOWN
    await engine.dispose()

    print("DB disconnected")