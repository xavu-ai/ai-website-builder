import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_submit_prompt_success(client):
    response = await client.post("/api/v1/prompts", json={"prompt": "Create a portfolio website"})
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()
    assert "confirmation_id" in data
    assert data["status"] == "queued"


@pytest.mark.asyncio
async def test_submit_prompt_empty(client):
    response = await client.post("/api/v1/prompts", json={"prompt": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_submit_prompt_whitespace_only(client):
    response = await client.post("/api/v1/prompts", json={"prompt": "   "})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_submit_prompt_too_long(client):
    long_prompt = "x" * 2001
    response = await client.post("/api/v1/prompts", json={"prompt": long_prompt})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_submit_prompt_max_length(client):
    max_prompt = "x" * 2000
    response = await client.post("/api/v1/prompts", json={"prompt": max_prompt})
    assert response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.asyncio
async def test_submit_prompt_missing_field(client):
    response = await client.post("/api/v1/prompts", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
