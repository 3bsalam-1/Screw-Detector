# ==============================================================================
# CONSOLIDATED IMPORTS FROM pipeline.ipynb
# ==============================================================================

# Standard library imports
import os
import json
import time
import random
import datetime
from pathlib import Path

# Third-party library imports
import numpy as np
import cv2
import yaml
import requests
import torch
import psutil
import matplotlib.pyplot as plt

# Model Detection and Prediction (Ultralytics & SAHI)
from ultralytics import YOLO
from sahi import AutoDetectionModel
from sahi.utils.cv import read_image
from sahi.predict import get_prediction, get_sliced_prediction

# ==============================================================================
# Setup verification
# ==============================================================================
print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")
print("All imports successful.")
