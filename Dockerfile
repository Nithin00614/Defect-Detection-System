FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Environment variables (clean + minimal)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    YOLO_TELEMETRY=false \
    YOLO_VERBOSE=false

# Install only required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (for better caching)
COPY requirements.txt .

# Upgrade pip and install dependencies (CPU only)
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Create required directories (avoid runtime issues)
RUN mkdir -p /app/temp /app/models/registry

# Expose ports
EXPOSE 8000 8501

# Start application
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]