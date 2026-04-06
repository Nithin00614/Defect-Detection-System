from ultralytics import YOLO

MODEL_PATH = "models/registry/model_v1.pt"

def evaluate():
    model = YOLO(MODEL_PATH)
    metrics = model.val(data="training/dataset.yaml")
    print(metrics)

if __name__ == "__main__":
    evaluate()
