from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from inference.predictor import DefectPredictor
from inference.schemas import PredictionResponse
import json
import os
import shutil
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Defect Detection API", version="2.0.0")

# Initialize predictor lazily
predictor = None


def get_predictor():
    global predictor
    if predictor is None:
        logger.info("Initializing predictor...")
        try:
            predictor = DefectPredictor()
            if predictor.model is None:
                logger.warning("⚠️ Predictor Initialized but model is unavailable")
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {e}")
            predictor = None
    return predictor


@app.on_event("startup")
async def startup():
    """Initialize predictor on startup."""
    logger.info("🚀 API Startup")
    get_predictor()
    logger.info("✅ API Ready")


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """Predict Defects in uploaded image."""
    temp_path = f"temp_{file.filename}"

    try:
        # Validate file
        if file.content_type is None or not file.content_type.startswith("image/"):
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid file type. Please upload an image."}
            )

        if file.size and file.size > 5 * 1024 * 1024:
            return JSONResponse(
                status_code=413,
                content={"error": "File too large (max 5MB)"}
            )

        # Save file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Get predictor
        pred = get_predictor()
        if pred is None or pred.model is None:
            return JSONResponse(
                status_code=503,
                content={"error": "Model not available. Service unavailable."}
            )

        # Run prediction
        detections = pred.predict(temp_path)
        logger.info(f"Processed image: {file.filename}, detections: {len(detections)}")

        return {"detections": detections}

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Prediction failed: {str(e)}"}
        )
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.get("/health")
def health():
    """Health check endpoint."""
    pred = get_predictor()
    status = "ok" if pred and pred.model else "degraded"
    return {
        "status": status,
        "model_loaded": pred.model is not None if pred else False
    }


@app.get("/model-info")
def model_info():
    """Get model information."""
    try:
        with open("models/registry/metadata.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Metadata not found"}
    except Exception as e:
        logger.error(f"Error reading metadata: {e}")
        return {"error": str(e)}


@app.get("/version")
def version():
    """Get version information."""
    pred = get_predictor()
    if pred and pred.model_path:
        return {"model": pred.model_path}
    return {"model": "unknown"}
