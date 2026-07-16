import json
import asyncio
from typing import Any, Optional
from utils.logger import setup_logger
from config.settings import get_settings

logger = setup_logger("cache")


class CacheManager:
    """
    Async Cache Manager with Redis primary and thread-safe in-memory dictionary fallback.
    """
    def __init__(self):
        self._redis = None
        self._memory_cache = {}
        self._lock = asyncio.Lock()
        self._redis_available = False

    async def connect(self):
        settings = get_settings()
        try:
            import redis.asyncio as redis
            self._redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
            await self._redis.ping()
            self._redis_available = True
            logger.info("Connected to Redis cache successfully.")
        except Exception as e:
            self._redis_available = False
            logger.info(f"Redis connection failed ({e}). Using in-memory fallback cache.")

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if self._redis_available and self._redis:
                try:
                    val = await self._redis.get(key)
                    if val is not None:
                        return json.loads(val)
                except Exception as e:
                    logger.debug(f"Redis get failed for {key}: {e}")
            return self._memory_cache.get(key)

    async def set(self, key: str, value: Any, ttl_seconds: int = 3600):
        async with self._lock:
            serialized = json.dumps(value, default=str)
            if self._redis_available and self._redis:
                try:
                    await self._redis.set(key, serialized, ex=ttl_seconds)
                    return
                except Exception as e:
                    logger.debug(f"Redis set failed for {key}: {e}")
            self._memory_cache[key] = value

    async def delete(self, key: str):
        async with self._lock:
            if self._redis_available and self._redis:
                try:
                    await self._redis.delete(key)
                except Exception:
                    pass
            self._memory_cache.pop(key, None)


cache_manager = CacheManager()
