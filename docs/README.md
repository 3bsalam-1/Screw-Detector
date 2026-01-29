# Documentation Directory

This directory contains comprehensive documentation for the Screw Detector project.

## Documentation Files

### Core Documentation

- **decision_log.md**: Architectural decisions and trade-offs made during development
  - Confidence threshold selection (0.6)
  - SAHI parameter optimization
  - Training resolution decisions
  - Edge deployment considerations

### Notebook Documentation

- **notebook_descriptions.md**: Descriptions for each section of the pipeline notebook
- **notebook_imports.py**: Consolidated imports for the notebook
- **notebook_optimized_content.md**: Optimized notebook cell contents
- **notebook_setup.py**: Notebook setup and installation instructions

## Documentation Structure

```
docs/
├── README.md                    # This file
├── decision_log.md              # Architectural decisions
├── notebook_descriptions.md     # Notebook section descriptions
├── notebook_imports.py           # Notebook imports
├── notebook_optimized_content.md # Optimized notebook content
└── notebook_setup.py             # Notebook setup
```

## Key Decisions Documented

### Confidence Threshold Selection
The most difficult decision was selecting an optimal confidence threshold of **0.6** for the SAHI inference pipeline. Through extensive hyperparameter optimization (testing 0.3-0.6 range), we found that **0.6** provided the best trade-off between Precision (94.7%) and Recall (97.5%), minimizing false positives while maintaining near-complete detection of tiny 10-15px screws.

### High-Resolution Training
Decision to train the YOLOv8s model at `imgsz=1280`:
- **Pro**: Better extraction of tiny features during feature map generation
- **Con**: Slower inference if used directly at full resolution
- **Mitigation**: Using SAHI slicing allows us to feed small patches (640x640) into the 1280-trained model, maintaining high resolution locally without the computational cost of a global 1280 image resize

### SAHI Implementation
Decision to implement SAHI with `slice_height=640` and `slice_width=640`:
- **Trade-off**: SAHI increases **Latency** (due to multiple forward passes over slices) but increases **Recall** on minuscule objects that are otherwise missed in global resizing
- **Result**: F1-score improved by ~4% over baseline, particularly in dense scenarios

### Edge Deployment via OpenVINO INT8
Decision to quantize models from FP32 to INT8 using OpenVINO:
- **Trade-off**: Possible slight drop in precision (~0.5-1%)
- **Result**: 2.5x - 3x speedup on CPU-based edge devices compared to standard ONNX Float32 inference, reducing per-image processing from ~5s to ~1.8s (including tiling)

## Usage

### Reading Documentation

All documentation files are written in Markdown format and can be viewed directly in any Markdown viewer or on GitHub.

### Linking Documentation

In the main [`README.md`](../README.md), documentation is linked using relative paths:
```markdown
See [Decision Log](docs/decision_log.md) for architectural decisions.
```

## Contributing to Documentation

When adding new documentation:
1. Use Markdown format
2. Include code examples where applicable
3. Add diagrams or visualizations for complex concepts
4. Update this README.md to reflect new documentation
5. Follow the project's documentation style

## Documentation Best Practices

1. **Be Clear**: Use simple, concise language
2. **Be Complete**: Include all necessary information
3. **Be Accurate**: Ensure all code examples work
4. **Be Organized**: Use consistent structure and formatting
5. **Be Up-to-Date**: Keep documentation synchronized with code changes

## Related Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [SAHI Documentation](https://github.com/obss/sahi)
- [OpenVINO Documentation](https://docs.openvino.ai/)
