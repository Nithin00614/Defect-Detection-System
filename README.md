
# 🚀 Industrial Defect Detection DL System – Real-Time Vision-Based Quality Inspection Pipeline

<p align="center">
  <img src="https://img.shields.io/badge/PyTorch-DeepLearning-red?logo=pytorch">
  <img src="https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi">
  <img src="https://img.shields.io/badge/Streamlit-UI-orange?logo=streamlit">
  <img src="https://img.shields.io/badge/Docker-Container-blue?logo=docker">
  <img src="https://img.shields.io/badge/AWS-EC2-yellow?logo=amazonaws">
</p>


## 📌 Overview

This project implements a **production-style deep learning defect detection system** demonstrating the complete model lifecycle, including training, versioned model registry, real-time inference, retraining pipelines, and deployment-ready APIs.

The system detects industrial surface defects using a YOLO-based object detection model and exposes a FastAPI inference service with a lightweight Streamlit visualization interface.

---

## Key Highlights

* End-to-end DL lifecycle (training → registry → inference → retraining)
* Versioned model registry with dynamic model loading
* Config-driven inference behavior
* Automated retraining and batch inference pipelines
* Observability endpoints for health and version tracking
* Visualization UI for interactive defect detection
* Docker-ready inference service

---

## Project Structure

```text
defect-detection-dl-system/
├── training/
├── inference/
├── pipelines/
├── models/registry/
├── streamlit_app.py
└── system_design.md
```

---

## 🌐 Deployment

Deployed on AWS EC2 using Docker with Elastic IP

- **Live App:** http://13.205.178.68:8501  
- **API Docs:** http://13.205.178.68:8000/docs  

---

## Running the Project

Start backend:

```bash
uvicorn inference.app:app --reload
```

Launch UI:

```bash
streamlit run streamlit_app.py
```
---

## Running with Docker
```bash
docker -compose up --build
```
---

## Dataset

The dataset is not included due to size.
Refer to external dataset and preprocessing pipeline for YOLO conversion.

---

## Tech Stack

- Python
- PyTorch / YOLO
- FastAPI
- Streamlit
- Docker

---
## Documentation

Detailed architecture, design decisions, lifecycle considerations, and failure analysis are available in:

👉**System Design:** [system_design.md](./system_design.md)

---
