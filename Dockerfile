FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    YOLOV5_AUTOINSTALL=false \
    YOLO_TELEMETRY=false \
    YOLO_VERBOSE=false

RUN apt-get update --fix-missing  && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/docker/entrypoint.sh

EXPOSE 8000 8501

ENTRYPOINT ["/bin/bash", "/app/docker/entrypoint.sh"]
