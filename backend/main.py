from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import prompts
from core.exceptions import PromptValidationError, QueueFullError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    print("Starting AI Website Builder API")
    yield
    print("Shutting down AI Website Builder API")


app = FastAPI(
    title="AI Website Builder API",
    description="Backend API for prompt submission and website generation",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(PromptValidationError)
async def prompt_validation_handler(
    request: Request, exc: PromptValidationError
) -> JSONResponse:
    """Handle prompt validation errors."""
    return JSONResponse(
        status_code=400,
        content={"error": "Validation error", "detail": exc.detail},
    )


@app.exception_handler(QueueFullError)
async def queue_full_handler(request: Request, exc: QueueFullError) -> JSONResponse:
    """Handle queue full errors."""
    return JSONResponse(
        status_code=503,
        content={"error": "Service unavailable", "detail": exc.detail},
    )


# Include API routes
app.include_router(prompts.router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
