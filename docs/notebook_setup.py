# ==============================================================================
# 1. INSTALLATION BLOCK
# ==============================================================================
# Run this once to ensure all dependencies are met for training and deployment
print("Installing project dependencies...")

!pip install -U ultralytics sahi openvino-dev nncf onnx onnxslim pyyaml psutil opencv-python matplotlib

# ==============================================================================
# 2. IMPORTS BLOCK
# ==============================================================================
# Standard library imports
import os
import time
import json
from pathlib import Path

# Data handling and visualization
import numpy as np
import cv2
import yaml
import psutil
import matplotlib.pyplot as plt

# Deep Learning and Model Detection
import torch
from ultralytics import YOLO
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction

# Environment verification
print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")
print("Setup Complete.")
