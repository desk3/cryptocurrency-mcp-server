FROM python:3.12-slim AS base

WORKDIR /app

# Install uv (dependency manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock README.md ./
COPY src/ src/

# Install dependencies
RUN uv sync --frozen --no-cache

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/src

EXPOSE 8100

# Start HTTP/SSE server on 0.0.0.0:8100
CMD ["uvicorn", "desk3_service.http_server:starlette_app", "--host", "0.0.0.0", "--port", "8100"] 
