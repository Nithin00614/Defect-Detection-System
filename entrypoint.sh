#!/bin/bash

set -e

echo "========================================"
echo "Defect Detection DL System - Starting"
echo "========================================"

# Set environment variables
export YOLO_TELEMETRY=false
export YOLO_VERBOSE=false
export PYTHONUNBUFFERED=1

# Cleanup function
cleanup() {
    echo ""
    echo "🧹 Cleaning up..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    rm -f temp_*.jpg temp_*.png temp_*.jpeg 2>/dev/null || true
    
    echo "Application stopped."
    exit 0
}

trap cleanup EXIT INT TERM

# Check model
if [ ! -f "models/registry/model_v1.pt" ]; then
    echo "⚠️  WARNING: Model not found at models/registry/model_v1.pt"
    echo "   The app will attempt to load available models."
fi

# Create temp directory
mkdir -p /app/temp

# Start FastAPI backend
echo ""
echo "[1/2] Starting FastAPI backend on port 8000..."
uvicorn inference.app:app --host 0.0.0.0 --port 8000 --log-level info 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend
echo "Waiting for backend startup..."
sleep 5

for i in {1..60}; do
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    if [ $i -eq 180 ]; then
        echo "❌ Backend failed to start within 180 seconds!"
        echo "Waiting longer..."
    fi
    sleep 1
done

# Start Streamlit
echo ""
echo "[2/2] Starting Streamlit on port 8501..."
export BACKEND_URL=http://localhost:8000/predict

streamlit run streamlit_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --logger.level=info 2>&1

