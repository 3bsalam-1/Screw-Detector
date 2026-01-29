# Notebook Annotations for pipeline.ipynb

This file contains markdown segments designed to be inserted above each code cell in the `pipeline.ipynb` notebook to match the style of `screw_detection_pipeline.ipynb`.

---

# Screw Detection Optimization: From Baseline to SAHI
## A Comprehensive Pipeline for Small Object Detection

This notebook documents the entire development cycle of a high-precision screw detection system. We address the challenge of detecting tiny objects (10-15px) within high-resolution images (1920x1080) using **YOLOv8** and **Slicing Aided Hyper Inference (SAHI)**.

---

## 1. Project Overview & Dataset Stats

The dataset consists of 250 images with over 8,000 annotations. We begin by analyzing the raw dataset metrics, focusing on class distribution and average object size.

---

## 2. Visual Ground Truth Verification

Before proceeding to inference or training, we verify the integrity of our labels. This cell visualizes random samples with their bounding boxes to confirm coordinate precision and class alignment.

---

## 3. Baseline YOLOv8 Inference (Global Resize)

We establish a performance ceiling using standard 1280px resized inference. This represents the "standard" path which often misses tiny 10-15px objects due to interpolation artifacts during downsampling.

---

## 4. SAHI Inference Implementation

To recover small objects, we implement **Slicing Aided Hyper Inference**. By processing the image in 640px slices at native resolution, we maintain the structural integrity of the smallest screw heads.

---

## 5. Hyperparameter Optimization Sweep

We perform a targeted grid search to find the optimal **Confidence** and **NMS** thresholds for SAHI. This ensures we maximize recall on the smallest objects while maintaining high precision.

---

## 6. Dataset Slicing for Native Training

We prepare the dataset for "Native Training" by slicing all source images into 640px overlapping tiles. This allows the model to learn features at the exact scale it will encounter during sliced inference.

---

## 7. Training the Sliced YOLOv8 Model

Using our 640px sliced dataset, we fine-tune the model. This step optimizes the weights specifically for small feature detection, moving away from global context to local detail.

---

## 8. Final Performance Benchmarking

A comprehensive comparison across all three strategies: **Baseline**, **Standard SAHI**, and **Sliced SAHI**. We measure Precision, Recall, and Latency to identify the production champion.

---

## 9. Size-Based Recall Analysis

To validate our logic, we analyze recall across three size bins: **Small (<15px)**, **Medium (15-30px)**, and **Large (>30px)**. This highlights the specific recovery rate for the most challenging objects.

---

## 10. Edge Optimization & Deployment (Raspberry Pi)

Final optimization for ARM-based hardware. We implement **Sequential Tiling** and **OpenVINO INT8** quantization to achieve real-time auditing speed within a strict 512MB RAM ceiling.

---

## Conclusion

The **Baseline 1280px** model offers high speed, but **Sliced SAHI** is the clear winner for accuracy on tiny objects. For edge deployment, **OpenVINO INT8** provides the necessary acceleration for low-power CPUs.
