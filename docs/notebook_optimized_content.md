# Industrial Fastener Detection: Screw, Nut, and Bolt Pipeline

This notebook documents the end-to-end pipeline for detecting industrial fasteners using state-of-the-art object detection models. The workflow covers dataset exploration, customized training strategies for small object detection, and hardware-accelerated deployment.

### Our Dataset Journey 🛠️
1. **Raw Source**: We started with the [raw, unannotated Screw/Washer Dataset](https://www.kaggle.com/datasets/wjybuqi/screwwasher-dataset-for-small-object-detection) from Kaggle.
2. **Annotation**: To ensure high-quality training, we manually annotated the dataset using **Roboflow**, specifically targeting the unique challenges of tiny industrial components.
3. **Public Release**: The final, fully annotated dataset was uploaded back to Kaggle to support the community: [Bolts and Washers Annotated Dataset](https://www.kaggle.com/datasets/ahmedmohamedab/bolts-and-washers).

---

## 1. Environment Setup and Dependencies

We leverage `ultralytics` for YOLOv8 model handling and `sahi` (Slicing Aided Hyper Inference) to enhance performance on small objects.

*(Code follows: Installation of ultralytics, sahi, openvino-dev)*

---

## 2. Dataset Exploration

The dataset consists of high-resolution images containing various industrial components. Accurate detection requires understanding the distribution of object sizes and classes.

**Key Objectives:**
- Load class definitions from `data.yaml`.
- Visualize ground truth labels on sample images.
- Analyze object size distribution (Small, Medium, Large).

---

## 3. Training Strategy 1: High-Resolution Baseline

To capture detail in complex scenes, we first train a **YOLOv8s** model using a high input resolution of **1280px**. This allows the model to process localized features without losing small object clarity to resizing.

**Hyperparameters:**
- Image size: 1280
- Epochs: 25
- Patience: 5

---

## 4. Training Strategy 2: Sliced Learning

Standard training often struggles when objects occupy <1% of the image area. In this approach, we pre-slice the training images into **640x640** overlaps. This effectively "zooms in" during the training phase, forcing the model to focus on micro-features of the fasteners.

---

## 5. Inference Methodologies

We compare two distinct inferencing techniques:

### A. Standard Inference
Standard single-pass detection on the full image. Fast, but may miss tiny objects if they are significantly downsampled.

### B. Slicing Aided Hyper Inference (SAHI)
SAHI divides the image into overlapping patches, runs inference on each patch, and merges the results. This significantly boosts the **Recall** of small objects at the cost of increased latency.

---

## 6. Performance Benchmarking and Evaluation

We evaluate the models across a standardized test set using:
- **Precision (P)**: Accuracy of positive predictions.
- **Recall (R)**: Ability to find all objects.
- **mAP@50**: Mean Average Precision at 0.5 IoU.

A custom evaluation suite provides a side-by-side comparison of baseline vs. optimized SAHI strategies.

---

## 7. Size-Based Recall Analysis

To better understand model failure modes, we bin performance metrics based on object size:
- **Small**: < 15px
- **Medium**: 15 - 30px
- **Large**: > 30px

This analysis validates that slicing techniques specifically recover "lost" small objects that standard detectors bypass.

---

## 8. Hardware Deployment and Edge Optimization

For real-world industrial deployment, we optimize the weights for CPU and Edge accelerators.

### Model Export
1. **ONNX**: Standard cross-platform format.
2. **OpenVINO INT8**: Quantized model specifically for Intel CPUs and VPUs, providing significant speedups for sequential tiling.

### Latency Benchmarking
We measure throughput (tiles/sec) and memory footprint to ensure the pipeline meets operational real-time requirements.

---

## 9. Conclusion and Recommendations

The results indicate that while the **1280px Baseline** is efficient for medium-to-large objects, **Sliced SAHI with OpenVINO acceleration** represents the most robust configuration for high-fidelity industrial inspection.
