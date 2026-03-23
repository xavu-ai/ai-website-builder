import json
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional

from core.config import settings


class QueueService(ABC):
    """Abstract base class for queue services."""

    @abstractmethod
    async def submit(self, prompt: str) -> str:
        """Submit a prompt to the queue."""
        pass

    @abstractmethod
    async def get_status(self, confirmation_id: str) -> Optional[dict[str, Any]]:
        """Get the status of a submission."""
        pass


class MemoryQueueService(QueueService):
    """In-memory queue service for prompt submissions."""

    def __init__(self) -> None:
        self._submissions: dict[str, dict[str, Any]] = {}

    async def submit(self, prompt: str) -> str:
        """Submit a prompt to the queue and return a confirmation ID."""
        if len(prompt.strip()) == 0:
            raise ValueError("Prompt cannot be empty or whitespace only")

        if len(prompt) > settings.MAX_PROMPT_LENGTH:
            raise ValueError(f"Prompt exceeds maximum length of {settings.MAX_PROMPT_LENGTH}")

        confirmation_id = str(uuid.uuid4())
        self._submissions[confirmation_id] = {
            "confirmation_id": confirmation_id,
            "prompt": prompt,
            "submitted_at": datetime.utcnow().isoformat(),
            "status": "queued",
        }
        return confirmation_id

    async def get_status(self, confirmation_id: str) -> Optional[dict[str, Any]]:
        """Get the status of a submission by confirmation ID."""
        return self._submissions.get(confirmation_id)


class RedisQueueService(QueueService):
    """Redis-based queue service for prompt submissions."""

    def __init__(self) -> None:
        import redis.asyncio as redis_lib
        self._redis: Optional[redis_lib.Redis] = None
        self._redis_lib = redis_lib

    async def _get_redis(self) -> Any:
        if self._redis is None:
            self._redis = self._redis_lib.from_url(
                settings.REDIS_URL, decode_responses=True
            )
        return self._redis

    async def submit(self, prompt: str) -> str:
        """Submit a prompt to the queue and return a confirmation ID."""
        if len(prompt.strip()) == 0:
            raise ValueError("Prompt cannot be empty or whitespace only")

        if len(prompt) > settings.MAX_PROMPT_LENGTH:
            raise ValueError(f"Prompt exceeds maximum length of {settings.MAX_PROMPT_LENGTH}")

        confirmation_id = str(uuid.uuid4())
        data = {
            "confirmation_id": confirmation_id,
            "prompt": prompt,
            "submitted_at": datetime.utcnow().isoformat(),
            "status": "queued",
        }
        r = await self._get_redis()
        await r.setex(f"prompt:{confirmation_id}", 3600, json.dumps(data))
        await r.lpush("prompt_queue", confirmation_id)
        return confirmation_id

    async def get_status(self, confirmation_id: str) -> Optional[dict[str, Any]]:
        """Get the status of a submission by confirmation ID."""
        r = await self._get_redis()
        data = await r.get(f"prompt:{confirmation_id}")
        return json.loads(data) if data else None


def get_queue_service() -> QueueService:
    """Get the appropriate queue service based on configuration."""
    if settings.REDIS_URL:
        return RedisQueueService()
    return MemoryQueueService()
