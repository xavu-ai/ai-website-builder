from fastapi import HTTPException, status


class PromptValidationError(HTTPException):
    """Raised when prompt validation fails."""

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "prompt_validation_error", "detail": detail},
        )


class QueueFullError(HTTPException):
    """Raised when the queue is full."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "queue_full", "detail": "Queue is full, please try again later"},
        )
