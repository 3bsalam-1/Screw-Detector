# Models Directory

This directory contains trained models for the Screw Detector project.

## Directory Structure

```
models/
├── .gitkeep              # Ensures directory is tracked by Git
├── yolov8s.pt            # Pretrained YOLOv8s model
├── yolov8s_1280_best.pt  # Best baseline model (1280px training)
├── yolov8s_1280_best.onnx # Exported ONNX model
├── yolov8_sliced_best.pt   # Best sliced model (640px training)
├── yolov8_sliced_best.onnx # Exported ONNX model
├── yolov8_sliced_best_int8_openvino_model/  # INT8 quantized OpenVINO model
└── yolov8s_1280_best_int8_openvino_model/  # INT8 quantized OpenVINO model
```

## Model Files

### Pretrained Models
- **yolov8s.pt**: Pretrained YOLOv8s model from Ultralytics

### Trained Models

#### Baseline Models (1280px Training)
- **yolov8s_1280_best.pt**: Best model trained at 1280px resolution
  - Training epochs: 150
  - Batch size: 4
  - Optimizer: AdamW
  - mAP@0.5: 90.92%
  - Precision: 89.9%
  - Recall: 95.0%

#### Sliced Models (640px Training)
- **yolov8_sliced_best.pt**: Best model trained on sliced dataset
  - Training epochs: 150
  - Batch size: 16
  - Optimizer: AdamW
  - mAP@0.5: 98.6% (on tiles)

### Exported Models

#### ONNX Models
- **yolov8s_1280_best.onnx**: Baseline model exported to ONNX
- **yolov8_sliced_best.onnx**: Sliced model exported to ONNX

#### OpenVINO Models
- **yolov8_sliced_best_int8_openvino_model/**: INT8 quantized OpenVINO model
  - Weight reduction: 22.5MB (FP32) → 10.9MB (INT8)
  - Speedup: 2.5x - 3x on CPU
- **yolov8s_1280_best_int8_openvino_model/**: INT8 quantized OpenVINO model

## Model Performance

| Model Strategy | Precision | Recall | F1-Score | Avg Time (ms) |
|---------------|-----------|--------|-----------|----------------|
| Baseline (1280 Resize) | 88.5% | 90.7% | 89.6% | ~85ms |
| Optimized SAHI (1280) | 92.4% | 94.2% | 93.3% | ~450ms |
| Sliced SAHI (640) | 85.1% | 87.8% | 86.4% | ~220ms |

### Size-Based Recall Recovery

SAHI significantly outperforms standard inference for the most challenging objects:

- **Small (<15px)**: ~80.6% recovery
- **Medium (15-30px)**: ~94.0% recovery
- **Large (>30px)**: ~97.6% recovery

## Usage

### Loading a Model

```python
from screw_detector.models import YOLOModel

# Load a trained model
model = YOLOModel("models/yolov8s_1280_best.pt")

# Load a pretrained model
model = YOLOModel.from_pretrained("yolov8s.pt")
```

### Exporting a Model

```bash
# Export to ONNX
screw-export --model models/yolov8s_1280_best.pt --format onnx

# Export to OpenVINO with INT8 quantization
screw-export --model models/yolov8s_1280_best.pt --format openvino --int8

# Export to all formats
screw-export --model models/yolov8s_1280_best.pt --format all
```

### Running Inference

```bash
# Baseline inference
screw-demo --model models/yolov8s_1280_best.pt --input image.jpg --strategy baseline

# SAHI inference
screw-demo --model models/yolov8s_1280_best.pt --input image.jpg --strategy sahi

# Compare strategies
screw-demo --model models/yolov8s_1280_best.pt --input image.jpg --strategy compare
```

## Model Sizes

| Model | Format | Size |
|--------|---------|-------|
| yolov8s.pt | PyTorch | ~22.5 MB |
| yolov8s_1280_best.pt | PyTorch | ~22.5 MB |
| yolov8s_1280_best.onnx | ONNX | ~22.5 MB |
| yolov8_sliced_best.pt | PyTorch | ~22.5 MB |
| yolov8_sliced_best.onnx | ONNX | ~22.5 MB |
| yolov8_sliced_best_int8_openvino_model/ | OpenVINO INT8 | ~10.9 MB |
| yolov8s_1280_best_int8_openvino_model/ | OpenVINO INT8 | ~10.9 MB |

## Notes

- Models are trained on the Bolts and Washers dataset
- For production use, consider using the baseline model for real-time applications
- For maximum accuracy, use SAHI inference with the baseline model
- For edge deployment, use the INT8 quantized OpenVINO models
- Model files should be added to `.gitignore` to prevent accidental commits
