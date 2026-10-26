from ultralytics import YOLO
import shutil
import yaml

MODEL_NAME = "yolov8n.pt"
OUTPUT_PATH = "models/registry/model_v2.pt"

with open("training/config.yaml") as f:
    config = yaml.safe_load(f)


def train():
    model = YOLO(MODEL_NAME)

    model.train(
        data="data.yaml",
        epochs=30,
        imgsz=640,
        batch=16
    )

    shutil.copy("runs/detect/train/weights/best.pt", OUTPUT_PATH)

if __name__ == "__main__":
    train()
