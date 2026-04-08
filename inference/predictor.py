import os
import yaml
import logging
import time

logger = logging.getLogger(__name__)

# Registry configuration
REGISTRY_PATH = "models/registry"
DEVICE = os.getenv("DEVICE", "cpu")

# Disable ultralytics telemetry BEFORE importing
os.environ['YOLO_TELEMETRY'] = 'false'
os.environ['YOLO_VERBOSE'] = 'false'

# Import after setting env vars
try:
    from ultralytics import YOLO
except ImportError as e:
    logger.error(f"Failed to import ultralytics: {e}")
    YOLO = None


def get_latest_model():
    """Load latest model version from registry safely."""
    try:
        if not os.path.exists(REGISTRY_PATH):
            os.makedirs(REGISTRY_PATH, exist_ok=True)
            logger.warning(f"Created registry directory: {REGISTRY_PATH}")
            
        models = [m for m in os.listdir(REGISTRY_PATH) if m.endswith(".pt")]

        if not models:
            logger.warning("No .pt model files found in registry")
            return None

        models.sort()
        model_path = os.path.join(REGISTRY_PATH, models[-1])
        logger.info(f"Found model: {model_path}")
        return model_path
    except Exception as e:
        logger.error(f"Error getting model: {e}", exc_info=True)
        return None


# Load inference configuration
def load_config():
    """Load configuration with defaults."""
    try:
        with open("training/config.yaml") as f:
            config = yaml.safe_load(f) or {}
            logger.info(f"Loaded config: {config}")
    except FileNotFoundError:
        logger.warning("config.yaml not found, using defaults")
        config = {}
    except Exception as e:
        logger.warning(f"Error loading config: {e}, using defaults")
        config = {}
    
    return config


# Predictor class
class DefectPredictor:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DefectPredictor, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        logger.info("Initializing DefectPredictor...")
        self.model = None
        self.model_path = None
        
        if YOLO is None:
            logger.error("Ultralytics YOLO not available")
            self._initialized = True
            return
        
        try:
            model_path = get_latest_model()
            if model_path and os.path.exists(model_path):
                logger.info(f"Loading model from: {model_path}")
                # Add retry logic for model loading
                for attempt in range(3):
                    try:
                        self.model = YOLO(model_path)
                        self.model.to(DEVICE)
                        self.model_path = model_path
                        logger.info(f"✅ Model loaded successfully on attempt {attempt + 1}")
                        break
                    except Exception as e:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}")
                        if attempt < 2:
                            time.sleep(1)
                        else:
                            raise
            else:
                logger.warning("No valid model path found")
        except Exception as e:
            logger.error(f"Failed to load model: {e}", exc_info=True)
            self.model = None
            self.model_path = None
        
        config = load_config()
        self.conf_threshold = config.get("conf_threshold", 0.5)
        logger.info(f"Confidence threshold: {self.conf_threshold}")
        
        self._initialized = True
        logger.info("DefectPredictor initialization complete")

    def predict(self, image_path):
        """Run defect detection and return filtered detections."""
        if not self.model:
            logger.error("Model not available for prediction")
            return []
            
        try:
            if not os.path.exists(image_path):
                logger.error(f"Image not found: {image_path}")
                return []
                
            logger.info(f"Running prediction on: {image_path}")
            results = self.model(image_path, device=DEVICE)[0]
            detections = []

            for box in results.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()

                if conf < self.conf_threshold:
                    continue

                detections.append({
                    "class_id": cls,
                    "confidence": conf,
                    "bbox": xyxy
                })
            
            logger.info(f"Found {len(detections)} detections (threshold: {self.conf_threshold})")
            return detections
        except Exception as e:
            logger.error(f"Prediction error: {e}", exc_info=True)
            return []
