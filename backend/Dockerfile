# syntax=docker/dockerfile:1

from python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock ./

# Install dependencies (using lockfile)
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Remove unnecessary files
RUN rm -rf tests


# Production stage
from python:3.11-slim

WORKDIR /app

# Create non-root user
RUN groupadd --gid 1000 appgroup && useradd --uid 1000 --gid 1000 --shell /bin/bash appuser

# Copy virtual environment from builder
COPY --from=builder /app .

# Change ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
