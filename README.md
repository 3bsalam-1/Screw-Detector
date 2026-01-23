# Screw Detection System: From Annotation to Edge Deployment

A high-precision object detection system for small screws, bolts, and washers. This project implements a complete pipeline starting from raw unannotated data to a deployment-ready model on Raspberry Pi, addressing the "tiny object" challenge using **YOLOv8** and **Slicing Aided Hyper Inference (SAHI)**.

---

## 🌟 Key Features
- **End-to-End Pipeline**: Covers manual annotation in Roboflow, dataset slicing, custom training, and edge optimization.
- **SAHI Integration**: Slicing ensures tiny objects (10x10px) are detected at native resolution without resizing loss.
- **Superior Precision**: Achieved **94.7% Precision** (55% reduction in false positives compared to baseline).
- **Edge Ready**: Includes INT8 quantized ONNX models and memory-efficient sequential inference for **Raspberry Pi 4/5**.
- **Boundary Resolution**: 20% tile overlap ensures objects cut in half at tile edges are accurately detected.

---

## 📝 Problem Statement & Dataset Journey
### The Challenge
Standard detectors normally resize 1920x1080 images down to 640x640, which shrinks 10px screws into ~3px blobs, making them unrecognizable. 

### The Journey
1. **Unannotated Data**: Started with raw images from Kaggle.
2. **Roboflow Annotation**: Manually labeled 225 images with precise bounding boxes for three classes: Bolt, Bottle, and Washer.
3. **Augmentation**: Applied rotation and noise to create a robust dataset of 225 train, 15 val, and 10 test images.
4. **Sliced Training**: To align the model with inference conditions, we sliced the training images into 640x640 tiles, generating ~1800 specialized training patches.

---

## 🛠️ Methodology: Sliced Training & SAHI
We implemented a **Slice -> Detect -> Merge** pipeline to maintain full pixel detail.

### 1. Slicing Strategy
- **Partial Object Filtering**: Discarded objects with <30% visibility to reduce label noise.
- **Empty Tile Strategy**: Kept ~20% "empty tiles" (negative samples) to explicitly train the model to suppress background false positives.

### 2. The "Screw Cut in Half" Problem
Tiling risks cutting objects at boundaries. 
- **Solution**: We implemented a **20% overlap**. This ensures that any object fragmented at the edge of Tile A is fully visible in the center of overlapping Tile B.
- **NMS Merging**: Overlapping detections are resolved using Non-Maximum Suppression (NMS) in the original image coordinate space.

---

## 📊 Performance Comparison
Evaluated on full-resolution (1920x1080) test images using an Intel Xeon W-2133 CPU.

| Approach | Precision | Recall | F1-Score | Latency | FP / FN Profile |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline (1280 Resize)** | 89.6% | **94.8%** | 92.1% | **474ms** | High False Positives (42) |
| **SAHI (Baseline Model)** | 91.2% | 90.6% | 90.9% | 6277ms | Better Stability |
| **SAHI (Sliced-Trained)** | **94.7%** | 88.2% | 91.3% | 1526ms | **Best Precision (19 FPs)** |

### Key Insight: 55% Reduction in False Positives
The Sliced-Trained model effectively eliminated "ghost" detections. By choosing a high confidence threshold (**0.7**), we prioritized **production stability** over raw recall to prevent false alarms from stopping industrial lines.

---

## 🍓 Raspberry Pi Deployment (Edge Optimization)
Deploying high-res slicing on edge hardware requires significant resource optimization.

### 1. Optimization Techniques
- **INT8 Quantization**: Reduced model size from 22.5MB to **10.9MB** and increased inference speed.
- **Tile Scaling (Pi-Lite)**: Reduced tile size to **416x416** to balance latency and heat.
- **Sequential Processing**: Modified the pipeline to process tiles one-by-one, keeping peak RAM usage below **80MB**.

### 2. Benchmarking (Estimated)
| Device | Latency per Image (1080p) | RAM Footprint | Optimized Path |
| :--- | :--- | :--- | :--- |
| **Raspberry Pi 5** | 1.5 - 2.0 sec | < 80 MB | INT8 ONNX |
| **Raspberry Pi 4** | 3.5 - 5.0 sec | < 80 MB | INT8 ONNX |

---

## 🚀 Getting Started

### Installation
```bash
# Clone the repository
git clone <repo-url>
cd screw-detector

# Install dependencies
pip install -r requirements.txt
```

### Usage
Run the unified inference pipeline on any image:
```bash
python scripts/inference_pipeline.py --input data/samples/sample1.jpg
```

For Raspberry Pi specific execution:
```bash
python scripts/raspberry_pi_inference.py
```

### Demonstration
Open `notebooks/screw_detection_complete_pipeline.ipynb` to see the full storytelling demo, including:
- Animation of tiling logic.
- Visual comparison of 0% vs 20% overlap.
- Step-by-step inference results.

---

## � Project Structure
- `notebooks/`: **`screw_detection_complete_pipeline.ipynb`** — The primary project story.
- `models/`: Trained weights (`.pt`) and `pi_optimized/` models (`.onnx`).
- `data/samples/`: Test images for demonstration.
- `results/`: Cached reports and performance benchmarks.
- `requirements.txt`: Project dependencies.

---

## 📚 Libraries
- `ultralytics` (YOLOv8)
- `sahi` (Slicing logic)
- `onnxruntime` (Edge inference)
- `opencv-python`, `torch`, `matplotlib`
