import redis
import json
from typing import Optional, Any
from app.config import settings


class CacheManager:
    def __init__(self):
        if settings.CACHE_ENABLED:
            self.redis_client = redis.from_url(
                settings.REDIS_URL, decode_responses=True
            )
        else:
            self.redis_client = None

    def get(self, key: str) -> Optional[Any]:
        if not self.redis_client:
            return None

        try:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            print(f"Cache get error: {e}")
        return None

    def set(self, key: str, value: Any, ttl: int = None):
        if not self.redis_client:
            return

        try:
            ttl = ttl or settings.CACHE_TTL
            self.redis_client.setex(key, ttl, json.dumps(value))
        except Exception as e:
            print(f"Cache set error: {e}")

    def delete(self, key: str):
        if not self.redis_client:
            return

        try:
            self.redis_client.delete(key)
        except Exception as e:
            print(f"Cache delete error: {e}")

    def clear_pattern(self, pattern: str):
        if not self.redis_client:
            return

        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Cache clear pattern error: {e}")


cache = CacheManager()
