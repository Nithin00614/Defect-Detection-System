from inference.predictor import DefectPredictor
import os

predictor = DefectPredictor()

image_dir = "batch_images"

for img in os.listdir(image_dir):
    result = predictor.predict(os.path.join(image_dir, img))
    print(img, result)
