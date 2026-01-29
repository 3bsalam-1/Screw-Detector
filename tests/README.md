# Tests Directory

This directory contains the test suite for the Screw Detector project.

## Test Structure

```
tests/
├── __init__.py           # Test package initialization
├── conftest.py           # Pytest fixtures and configuration
├── test_dataset.py        # Dataset module tests
├── test_inference.py      # Inference module tests
├── test_models.py         # Models module tests
└── test_utils.py          # Utils module tests
```

## Running Tests

### Run All Tests

```bash
# From project root
pytest
```

### Run Specific Test File

```bash
# Run only dataset tests
pytest tests/test_dataset.py

# Run only inference tests
pytest tests/test_inference.py
```

### Run with Coverage

```bash
# Generate coverage report
pytest --cov=src/screw_detector --cov-report=html

# Open coverage report
open htmlcov/index.html
```

### Run Specific Test

```bash
# Run a specific test function
pytest tests/test_inference.py::TestCalculateIoU::test_perfect_overlap

# Run tests matching a pattern
pytest -k "iou"
```

### Run with Verbose Output

```bash
# Show detailed test output
pytest -v

# Show even more detailed output
pytest -vv
```

## Test Coverage

The project aims for:
- **Overall Coverage**: >80%
- **New Features**: >90% coverage
- **Critical Paths**: 100% coverage

## Test Files

### conftest.py
Pytest configuration and fixtures:
- `project_root`: Project root directory fixture
- `data_dir`: Data directory fixture
- `configs_dir`: Configs directory fixture
- `test_data_dir`: Test data directory fixture
- `sample_image_path`: Sample test image fixture
- `sample_label_path`: Sample test label fixture
- `temp_dir`: Temporary directory fixture
- `sample_config_dict`: Sample configuration fixture
- `sample_detections`: Sample detection results fixture
- `sample_ground_truth`: Sample ground truth fixture

### test_dataset.py
Tests for dataset module:
- `DatasetStats` class tests
- Dataset validation tests
- Dataset slicing tests

### test_inference.py
Tests for inference module:
- `calculate_iou` function tests
- `match_detections` function tests
- `BaselineInference` class tests
- `SAHIInference` class tests

### test_models.py
Tests for models module:
- `YOLOModel` class tests
- `ModelTrainer` class tests
- `ModelExporter` class tests
- `get_model_size` function tests
- `list_available_models` function tests

### test_utils.py
Tests for utils module:
- `calculate_metrics` function tests
- `calculate_size_based_recall` function tests
- `get_image_size` function tests
- `load_ground_truth` function tests

## Test Markers

Tests can be marked with custom markers:

```bash
# Run only fast tests
pytest -m "not slow"

# Run only integration tests
pytest -m "integration"
```

## Writing Tests

### Test Structure

Follow the Arrange-Act-Assert pattern:

```python
def test_calculate_iou_perfect_overlap():
    """Test IoU calculation with perfect overlap."""
    # Arrange
    box1 = [0, 0, 100, 100]
    box2 = [0, 0, 100, 100]
    
    # Act
    iou = calculate_iou(box1, box2)
    
    # Assert
    assert iou == pytest.approx(1.0)
```

### Best Practices

1. **Descriptive Names**: Use clear, descriptive test names
2. **One Assertion Per Test**: Keep tests focused
3. **Use Fixtures**: Reuse common test data
4. **Test Edge Cases**: Include boundary conditions
5. **Mock External Dependencies**: Don't rely on external resources

### Skipping Tests

Tests can be conditionally skipped:

```python
@pytest.mark.skipif(
    not Path("models/yolov8s.pt").exists(),
    reason="Model file not found"
)
def test_model_loading():
    """Test model loading."""
    # Test implementation
```

## Continuous Integration

Tests run automatically on:
- **Push to main/develop**: Full test suite
- **Pull Requests**: Full test suite
- **Multiple Python Versions**: 3.9, 3.10, 3.11

See [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) for CI configuration.

## Troubleshooting

### Common Issues

**Issue**: Tests fail with import errors
- **Solution**: Install package in development mode: `pip install -e .`

**Issue**: Tests fail with model not found
- **Solution**: Download pretrained model or skip model-dependent tests

**Issue**: Tests fail with data not found
- **Solution**: Ensure dataset is in correct location

## Contributing Tests

When adding new functionality:
1. Write tests first (TDD approach)
2. Ensure tests cover edge cases
3. Aim for high code coverage
4. Update this README for new test files

## Related Documentation

- [Contributing Guide](../CONTRIBUTING.md)
- [Pytest Documentation](https://docs.pytest.org/)
- [Project README](../README.md)
