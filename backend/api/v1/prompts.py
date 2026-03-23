from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from models.prompt import PromptSubmissionRequest, PromptSubmissionResponse
from services.queue import get_queue_service

router = APIRouter(prefix="/prompts", tags=["prompts"])
queue_service = get_queue_service()


@router.post(
    "",
    response_model=PromptSubmissionResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit a prompt for processing"
)
async def submit_prompt(request: PromptSubmissionRequest):
    try:
        confirmation_id = await queue_service.submit(request.prompt)
        return PromptSubmissionResponse(
            confirmation_id=confirmation_id,
            status="queued",
            submitted_at=datetime.utcnow(),
            estimated_processing_time="30s"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to queue prompt: {str(e)}"
        )
