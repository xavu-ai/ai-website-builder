import pytest
from services.queue import MemoryQueueService


@pytest.mark.asyncio
async def test_memory_queue_submit():
    service = MemoryQueueService()
    confirmation_id = await service.submit("test prompt")
    assert confirmation_id is not None
    assert len(confirmation_id) > 0


@pytest.mark.asyncio
async def test_memory_queue_get_status():
    service = MemoryQueueService()
    confirmation_id = await service.submit("test prompt")
    status = await service.get_status(confirmation_id)
    assert status is not None
    assert status["prompt"] == "test prompt"
    assert status["status"] == "queued"


@pytest.mark.asyncio
async def test_memory_queue_get_status_not_found():
    service = MemoryQueueService()
    status = await service.get_status("non-existent-id")
    assert status is None
