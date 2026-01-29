"""
Pytest configuration and fixtures for Screw Detector tests.
"""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def data_dir(project_root):
    """Get the data directory."""
    return project_root / "data"


@pytest.fixture
def configs_dir(data_dir):
    """Get the configs directory."""
    return data_dir / "configs"


@pytest.fixture
def raw_data_dir(data_dir):
    """Get the raw data directory."""
    return data_dir / "raw"


@pytest.fixture
def test_data_dir(raw_data_dir):
    """Get the test data directory."""
    return raw_data_dir / "test"


@pytest.fixture
def sample_image_path(test_data_dir):
    """Get a sample test image path."""
    images = list(test_data_dir.glob("*.jpg"))
    if images:
        return images[0]
    return None


@pytest.fixture
def sample_label_path(test_data_dir):
    """Get a sample test label path."""
    labels = list((test_data_dir.parent / "labels").glob("*.txt"))
    if labels:
        return labels[0]
    return None


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp, ignore_errors=True)


@pytest.fixture
def sample_config_dict():
    """Sample configuration dictionary for testing."""
    return {
        "names": ["Bolt", "Bottle", "Washer"],
        "nc": 3,
        "train": "data/raw/train/images",
        "val": "data/raw/valid/images",
        "test": "data/raw/test/images"
    }


@pytest.fixture
def sample_detections():
    """Sample detection results for testing."""
    return [
        {
            "class_id": 0,
            "class_name": "Bolt",
            "confidence": 0.95,
            "bbox": [100, 100, 200, 200]
        },
        {
            "class_id": 2,
            "class_name": "Washer",
            "confidence": 0.87,
            "bbox": [300, 150, 400, 250]
        }
    ]


@pytest.fixture
def sample_ground_truth():
    """Sample ground truth annotations for testing."""
    return [
        {
            "class_id": 0,
            "bbox": [105, 105, 195, 195]
        },
        {
            "class_id": 2,
            "bbox": [305, 155, 395, 245]
        }
    ]
