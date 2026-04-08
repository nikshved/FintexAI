# app/db/redis.py
import redis.asyncio as redis

# Один пул на все приложение (создается при импорте)
pool = redis.ConnectionPool.from_url("redis://localhost", decode_responses=True)


async def get_redis():
    client = redis.Redis(connection_pool=pool)
    try:
        yield client
    finally:
        await client.close()
