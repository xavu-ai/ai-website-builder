from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class PromptSubmissionRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)

    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('prompt cannot be empty or whitespace only')
        return v.strip()


class PromptSubmissionResponse(BaseModel):
    confirmation_id: UUID
    status: str = "queued"
    submitted_at: datetime
    estimated_processing_time: str = "30s"
