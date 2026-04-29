#!/bin/bash

set -e

echo "========================================"
echo "Defect Detection DL System - Starting"
echo "========================================"

# Environment variables
export YOLO_TELEMETRY=false
export YOLO_VERBOSE=false
export PYTHONUNBUFFERED=1

# Cleanup function
cleanup() {
    echo ""
    echo "🧹 Cleaning up..."

    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi

    rm -f /app/temp/temp_*.jpg /app/temp/temp_*.png /app/temp/temp_*.jpeg 2>/dev/null || true

    echo "Application stopped."
    exit 0
}

trap cleanup EXIT INT TERM

# ✅ FIXED: Absolute path for model
MODEL_PATH="/app/models/registry/model_v1.pt"

if [ ! -f "$MODEL_PATH" ]; then
    echo "⚠️ WARNING: Model not found at $MODEL_PATH"
    echo "   The app will attempt to load available models."
else
    echo "✅ Model found: $MODEL_PATH"
fi

# Create temp directory
mkdir -p /app/temp

# Start FastAPI backend
echo ""
echo "[1/2] Starting FastAPI backend on port 8000..."

uvicorn inference.app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level warning &

BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend (optimized)
echo "Waiting for backend startup..."

for i in {1..60}; do
    if curl -fs http://127.0.0.1:8000/health > /dev/null; then
        echo "✅ Backend is ready!"
        break
    fi
    sleep 1
done

# If backend still not ready → fail early
if ! curl -fs http://127.0.0.1:8000/health > /dev/null; then
    echo "❌ Backend failed to start!"
    exit 1
fi

# Start Streamlit
echo ""
echo "[2/2] Starting Streamlit on port 8501..."

export BACKEND_URL=http://127.0.0.1:8000/predict

exec streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --logger.level=warning