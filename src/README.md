# Source Directory

This directory contains the source code for the Screw Detector project.

## Directory Structure

```
src/
├── screw_detector/   # Main package
│   ├── __init__.py       # Package initialization
│   ├── config.py          # Configuration management
│   ├── dataset.py         # Dataset utilities
│   ├── inference.py       # Inference utilities
│   ├── models.py          # Model utilities
│   ├── sahi_utils.py      # SAHI utilities
│   └── utils.py           # Common utilities
└── scripts/              # Command-line scripts
    ├── train.py           # Training script
    ├── evaluate.py        # Evaluation script
    ├── export.py          # Export script
    ├── demo.py            # Demo script
    └── slice_dataset.py   # Dataset slicing script
```

## Package: screw_detector

The main package provides a Python API for screw detection.

### Installation

```bash
# Install from source
pip install -e .

# Install in development mode
pip install -e ".[dev]"
```

### Usage

```python
from screw_detector import Config, DatasetStats, SAHIInference

# Load configuration
config = Config()

# Get dataset statistics
stats = DatasetStats("data/configs/data.yaml")
stats.print_stats()

# Run SAHI inference
inference = SAHIInference("models/yolov8s.pt", config=config.sahi)
detections = inference.predict("image.jpg")
```

## Package Modules

### config.py
Configuration management for training, inference, and dataset operations.

**Classes:**
- `Config`: Main configuration class
- `SAHIConfig`: SAHI inference configuration
- `TrainingConfig`: Training configuration
- `SlicingConfig`: Dataset slicing configuration
- `ExportConfig`: Model export configuration

**Functions:**
- `load_config()`: Load configuration from YAML
- `get_data_config()`: Load dataset configuration

### dataset.py
Dataset utilities for statistics, validation, and slicing.

**Classes:**
- `DatasetStats`: Dataset statistics calculator

**Functions:**
- `slice_yolo_dataset()`: Slice dataset into tiles
- `validate_dataset()`: Validate dataset integrity
- `print_validation_results()`: Print validation results

### inference.py
Inference utilities for baseline and SAHI detection.

**Classes:**
- `BaselineInference`: Baseline YOLOv8 inference
- `SAHIInference`: SAHI-enhanced inference

**Functions:**
- `compare_inference()`: Compare baseline and SAHI
- `visualize_predictions()`: Visualize detections
- `visualize_comparison()`: Visualize comparison
- `calculate_iou()`: Calculate Intersection over Union
- `match_detections()`: Match predictions with ground truth

### models.py
Model utilities for training, loading, and exporting.

**Classes:**
- `YOLOModel`: YOLOv8 model wrapper
- `ModelTrainer`: Model training wrapper
- `ModelExporter`: Model export wrapper

**Functions:**
- `get_model_size()`: Get model file size
- `list_available_models()`: List available pretrained models

### sahi_utils.py
SAHI-specific utilities for optimization and prediction.

**Classes:**
- `SAHIPredictor`: SAHI predictor wrapper

**Functions:**
- `get_sliced_prediction()`: Run SAHI prediction
- `optimize_sahi_parameters()`: Optimize SAHI parameters
- `calculate_slice_count()`: Calculate number of slices

### utils.py
Common utilities for visualization and metrics.

**Functions:**
- `visualize_predictions()`: Visualize detections on image
- `visualize_comparison()`: Visualize baseline vs SAHI
- `calculate_metrics()`: Calculate evaluation metrics
- `calculate_size_based_recall()`: Calculate size-based recall
- `plot_metrics_comparison()`: Plot metrics comparison
- `plot_size_based_recall()`: Plot size-based recall
- `create_results_table()`: Create results table
- `print_results_table()`: Print results table
- `get_image_size()`: Get image dimensions
- `load_ground_truth()`: Load ground truth annotations

## Scripts

### train.py
Command-line interface for training YOLOv8 models.

```bash
# Train baseline model
python -m src.scripts.train --model yolov8s.pt --data data/configs/data.yaml

# Train on sliced dataset
python -m src.scripts.train --model yolov8s.pt --sliced-data
```

### evaluate.py
Command-line interface for evaluating models.

```bash
# Evaluate with both strategies
python -m src.scripts.evaluate --model models/best.pt --strategy both --save-plots
```

### export.py
Command-line interface for exporting models.

```bash
# Export to ONNX
python -m src.scripts.export --model models/best.pt --format onnx

# Export to OpenVINO with INT8
python -m src.scripts.export --model models/best.pt --format openvino --int8
```

### demo.py
Command-line interface for running inference demos.

```bash
# Run SAHI demo
python -m src.scripts.demo --model models/best.pt --input image.jpg --strategy sahi

# Compare strategies
python -m src.scripts.demo --model models/best.pt --input image.jpg --strategy compare
```

### slice_dataset.py
Command-line interface for slicing datasets.

```bash
# Slice dataset
python -m src.scripts.slice_dataset --data data/configs/data.yaml --validate
```

## Development

### Adding New Modules

1. Create module file in `screw_detector/`
2. Add imports to `__init__.py`
3. Write module with docstrings
4. Add tests in `tests/`
5. Update documentation

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Maximum line length: 100 characters

### Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src/screw_detector
```

## Related Documentation

- [Project README](../README.md)
- [Tests README](../tests/README.md)
- [Contributing Guide](../CONTRIBUTING.md)
