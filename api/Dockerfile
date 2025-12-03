FROM python:3.11-slim AS builder

WORKDIR /app

# Copy application code
COPY ./src/ ./src/
COPY ./database/ ./database/
COPY ./pyproject.toml .

FROM python:3.11-slim

WORKDIR /app

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy application code from builder
COPY --from=builder /app/src ./src
COPY --from=builder /app/database ./database

# Install dependencies (after copying source code)
COPY ./pyproject.toml .
RUN pip install --no-cache-dir .

# Application environment variables
ENV PORT=3000 \
    DATABASE_PATH=/app/data/supply_chain.db \
    PYTHON_ENV=production

# Create data directory and set permissions
RUN mkdir -p /app/data && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 3000

# Use exec form and shell wrapper for environment variable substitution
CMD ["sh", "-c", "api-init-db --seed && exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]
