import json
from abc import ABC, abstractmethod
from typing import Any, Optional

from aioredis import Redis

EXPIRE = 30


class CacheService(ABC):

    @abstractmethod
    async def set_value(self, key: str, data: Any):
        pass

    @abstractmethod
    async def get_value(self, api_name: str) -> Any:
        pass


class RedisService(CacheService):

    def __init__(self, redis: Redis):
        self._redis = redis

    async def set_value(self, key: str, data: Any):
        json_data = json.dumps(data)
        return await self._redis.set(
            name=key,
            value=json_data,
            ex=EXPIRE,
        )

    async def get_value(self, key: str) -> Any:
        if cache := await self._redis.get(key):
            return json.loads(cache)
        return None

    async def delete_key(self, key: str):
        self._redis.delete(key)

    async def delete_by_value(self, session_id: str) -> Optional[bool]:
        keys = await self._redis.keys("*")
        for key in keys:
            val = await self._redis.get(key)
            val = val.decode("utf-8")
            if val == session_id:
                self._redis.delete(key)
                return True

    async def get_key_by_value(self, session_id: str) -> Optional[str]:
        keys = await self._redis.keys("*")
        for key in keys:
            val = await self._redis.get(key)
            val = val.decode("utf-8")
            if val == session_id:
                return key.decode("utf-8")
