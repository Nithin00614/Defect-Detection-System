import os
from training.train import train

def retrain():
    print("Starting retraining...")
    train()
    print("Retraining complete and new model promoted")

if __name__ == "__main__":
    retrain()
