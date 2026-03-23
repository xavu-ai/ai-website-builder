import json
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
import redis.asyncio as redis
from core.config import settings


class QueueService(ABC):
    @abstractmethod
    async def submit(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def get_status(self, confirmation_id: str) -> Optional[dict]:
        pass


class MemoryQueueService(QueueService):
    def __init__(self):
        self._queue = {}

    async def submit(self, prompt: str) -> str:
        confirmation_id = str(uuid.uuid4())
        self._queue[confirmation_id] = {
            "prompt": prompt,
            "status": "queued",
            "submitted_at": datetime.utcnow().isoformat(),
        }
        return confirmation_id

    async def get_status(self, confirmation_id: str) -> Optional[dict]:
        return self._queue.get(confirmation_id)


class RedisQueueService(QueueService):
    def __init__(self):
        self._redis: Optional[redis.Redis] = None

    async def _get_redis(self) -> redis.Redis:
        if self._redis is None:
            self._redis = redis.from_url(settings.redis_url, decode_responses=True)
        return self._redis

    async def submit(self, prompt: str) -> str:
        confirmation_id = str(uuid.uuid4())
        data = {
            "prompt": prompt,
            "status": "queued",
            "submitted_at": datetime.utcnow().isoformat(),
        }
        r = await self._get_redis()
        await r.setex(f"prompt:{confirmation_id}", 3600, json.dumps(data))
        await r.lpush("prompt_queue", confirmation_id)
        return confirmation_id

    async def get_status(self, confirmation_id: str) -> Optional[dict]:
        r = await self._get_redis()
        data = await r.get(f"prompt:{confirmation_id}")
        return json.loads(data) if data else None


def get_queue_service() -> QueueService:
    if settings.redis_url and settings.redis_url.startswith("redis://"):
        return RedisQueueService()
    return MemoryQueueService()
