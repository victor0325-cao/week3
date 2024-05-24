from redis import asyncio as aioredis
from config import config

def make_redis(conf):
    connection_pool = aioredis.connection.ConnectionPool.from_url(
        f"redis://{conf.host}:{conf.port}/{conf.db}",
    )

    redis = aioredis.Redis(
        connection_pool=connection_pool,
        decode_responses=True
    )

    return redis

redis_cli = make_redis(config.cache)
