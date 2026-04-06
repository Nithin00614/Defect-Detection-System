import streamlit as st
import requests
import time
import os
from PIL import Image, ImageDraw

# Backend URL - use environment variable or default
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/predict")

CLASS_NAMES = [
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches"
]

st.set_page_config(page_title="Defect Detection", layout="centered")

st.title("🔎 Industrial Surface Defect Detection")

uploaded_file = st.file_uploader(
    "Upload defect image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", width=700)

    uploaded_file.seek(0)

    # ---- Backend call with latency ----
    try:
        start = time.time()
        response = requests.post(
            BACKEND_URL,
            files={"file": (uploaded_file.name, uploaded_file, "image/jpeg")},
            timeout=20
        )
        latency = time.time() - start
    except Exception as e:
        st.error(f"Backend connection failed: {e}")
        st.stop()

    if response.status_code != 200:
        st.error(f"Backend error (status {response.status_code})")
        st.stop()

    try:
        data = response.json()
    except Exception:
        st.error("Invalid backend response")
        st.stop()

    if "error" in data:
        st.error(data["error"])
        st.stop()

    st.caption(f"Inference latency: {latency:.2f}s")

    if len(data.get("detections", [])) == 0:
        st.warning("No defects detected (low confidence)")
        st.stop()

    # ---- Draw detections ----
    draw = ImageDraw.Draw(image)

    for det in data["detections"]:
        bbox = det["bbox"]
        conf = det["confidence"]
        cls = det["class_id"]

        label = CLASS_NAMES[cls]

        draw.rectangle(bbox, outline="red", width=3)
        draw.text((bbox[0], bbox[1]), f"{label} {conf:.2f}", fill="red")

    st.image(image, caption="Detected Defects", width=700)

    st.subheader("Detection JSON") 
    st.json(data)