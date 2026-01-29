# Notebooks Directory

This directory contains Jupyter notebooks for the Screw Detector project.

## Available Notebooks

### 01_pipeline.ipynb
Complete pipeline notebook covering the entire development cycle of the screw detection system.

**Sections:**
1. Project Overview & Dataset Stats
2. Visual Ground Truth Verification
3. Baseline YOLOv8 Inference (Global Resize)
4. SAHI Inference Implementation
5. Hyperparameter Optimization Sweep
6. Dataset Slicing for Native Training
7. Training the Sliced YOLOv8 Model
8. Final Performance Benchmarking
9. Size-Based Recall Analysis
10. Edge Optimization & Deployment (Raspberry Pi)

## Running Notebooks

### Prerequisites

```bash
# Install Jupyter and dependencies
pip install jupyterlab ipykernel

# Install project dependencies
pip install -r ../requirements.txt
```

### Starting Jupyter

```bash
# From project root
jupyter lab notebooks/
```

Or using VS Code:
1. Open the notebook file
2. Select the kernel (Python 3.9+)

## Notebook Structure

Each notebook follows a consistent structure:

### 1. Setup and Imports
- Install required packages
- Import necessary libraries
- Verify environment setup

### 2. Data Exploration
- Load dataset configuration
- Calculate statistics
- Visualize sample data

### 3. Model Training
- Configure training parameters
- Train YOLOv8 models
- Monitor training progress

### 4. Inference and Evaluation
- Run baseline inference
- Implement SAHI inference
- Compare performance
- Analyze results

### 5. Visualization
- Plot training curves
- Visualize predictions
- Generate comparison charts

## Key Concepts Covered

### YOLOv8
- Model architecture
- Training configuration
- Hyperparameter tuning
- Model export (ONNX, OpenVINO)

### SAHI (Slicing Aided Hyper Inference)
- Image slicing strategy
- Overlap parameters
- NMS post-processing
- Performance optimization

### Small Object Detection
- Challenges with tiny objects (10-15px)
- Size-based recall analysis
- Optimization techniques

### Edge Deployment
- Model quantization (FP32 → INT8)
- OpenVINO optimization
- Raspberry Pi deployment
- Performance benchmarking

## Performance Benchmarks

The notebooks demonstrate the following performance metrics:

| Model Strategy | Precision | Recall | F1-Score | Avg Time (ms) |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline (1280 trained, resized 640)** | 88.5% | 90.7% | 89.6% | ~85ms |
| **Optimized SAHI (1280 model)** | 92.4% | 94.2% | 93.3% | ~450ms |
| **Sliced SAHI (640 model)** | 85.1% | 87.8% | 86.4% | ~220ms |

### Size-Based Recall Recovery

SAHI significantly outperforms standard inference for the most challenging objects:
- **Small (<15px)**: ~80.6% recovery
- **Medium (15-30px)**: ~94.0% recovery
- **Large (>30px)**: ~97.6% recovery

## Tips for Using Notebooks

1. **Run Cells Sequentially**: Execute cells in order to ensure dependencies are met
2. **Save Outputs**: Save important results and visualizations
3. **Adjust Parameters**: Modify hyperparameters based on your hardware
4. **Monitor Resources**: Watch GPU/CPU usage during training
5. **Document Changes**: Note any modifications you make to the notebook

## Exporting Results

Notebooks can export results in various formats:
- **CSV**: For data analysis
- **PNG**: For visualizations
- **ONNX/OpenVINO**: For model deployment

## Troubleshooting

### Common Issues

**Issue**: CUDA out of memory
- **Solution**: Reduce batch size or image size

**Issue**: Slow training
- **Solution**: Use smaller model (yolov8n) or reduce epochs

**Issue**: Poor detection on small objects
- **Solution**: Use SAHI inference or train on sliced dataset

## Related Documentation

- [Main README](../README.md)
- [Documentation](../docs/README.md)
- [Contributing Guide](../CONTRIBUTING.md)
