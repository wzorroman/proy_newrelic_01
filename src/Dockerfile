# FROM python:3.11-slim
FROM python_newrelic:latest

WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     bzip2-dev \
#     gcc \
#     curl \
#     libc-dev \
#     libffi-dev \
#     libressl-dev \
#     linux-headers \
#     && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    curl \
    && rm -rf /var/cache/apk/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# # Create non-root user - Modo slim
# RUN groupadd -r fastapi && useradd -r -g fastapi fastapi
# RUN chown -R fastapi:fastapi /app
# USER fastapi

# Create non-root user (CORREGIDO para Alpine)
RUN addgroup -S fastapi && adduser -S fastapi -G fastapi
RUN chown -R fastapi:fastapi /app
USER fastapi

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
