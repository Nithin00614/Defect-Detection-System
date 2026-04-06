
## 1. Problem

Design a production-ready deep learning system for industrial surface defect detection supporting real-time inference and controlled model lifecycle management.

---

## 2. Architecture

### Offline Layer

* annotation normalization (VOC → YOLO)
* GPU-based training pipeline
* model evaluation and artifact generation

### Model Registry

* versioned model artifacts
* safe promotion and rollback

### Online Inference

* FastAPI prediction service
* dynamic model loading
* request validation and confidence filtering

### Lifecycle Management

* retraining pipeline
* batch inference validation
* observability endpoints (health, version, metadata)

---

## 3. Key Design Decisions

**Training–Inference Separation**
Avoid GPU dependency during deployment.

**Model Registry Versioning**
Enable safe model replacement without redeploying inference service.

**Config-Driven Inference**
Allows threshold tuning without code changes.

**Annotation Normalization**
Ensures dataset consistency for reliable training.

---

## 4. Constraints

* GPU required for training
* inference latency vs accuracy trade-off
* dataset annotation quality impact

---

## 5. Failure Modes

* corrupted image uploads
* empty detections due to low confidence
* incompatible model artifact
* annotation preprocessing errors

---

## 6. Future Improvements

* drift detection
* active learning loop
* streaming inference
* edge deployment optimization

---
