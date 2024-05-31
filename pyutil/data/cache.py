from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

def init(conf):
    redis = aioredis.from_url(f"redis://{conf.host}:{conf.port}/{conf.db}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="healux-admin-cache")

