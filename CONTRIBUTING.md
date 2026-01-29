# Contributing to Screw Detector

Thank you for your interest in contributing to Screw Detector! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to 3bsalam0@gmail.com.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- A GitHub account

### Setting Up Development Environment

1. **Fork the repository**

   ```bash
   # Fork the repository on GitHub
   git clone https://github.com/3bsalam-1/Screw-Detector.git
   cd Screw-Detector
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**

   ```bash
   pre-commit install
   ```

5. **Run tests to verify setup**

   ```bash
   pytest
   ```

## Development Workflow

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Urgent fixes for production

### Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Making Changes

1. Write code following the [Coding Standards](#coding-standards)
2. Add tests for new functionality
3. Ensure all tests pass: `pytest`
4. Run linting: `ruff check src/ tests/`
5. Format code: `black src/ tests/`
6. Commit changes with clear messages

### Commit Message Format

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(inference): add support for custom SAHI parameters

Add ability to pass custom slice size and overlap ratios
to SAHI inference for better control over detection
performance.

Closes #123
```

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Maximum line length: 100 characters

### Code Formatting

We use:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

These are automatically run by pre-commit hooks.

### Documentation

- Use Google-style docstrings
- Include parameter and return type information
- Add examples for complex functions

Example:
```python
def calculate_iou(box1: List[float], box2: List[float]) -> float:
    """Calculate Intersection over Union (IoU) between two bounding boxes.
    
    Args:
        box1: First bounding box [x1, y1, x2, y2].
        box2: Second bounding box [x1, y1, x2, y2].
        
    Returns:
        IoU value between 0 and 1.
        
    Example:
        >>> calculate_iou([0, 0, 100, 100], [0, 0, 100, 100])
        1.0
    """
    # Implementation
```

## Testing

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Use fixtures for common test data

Example:
```python
def test_calculate_iou_perfect_overlap():
    """Test IoU calculation with perfect overlap."""
    box1 = [0, 0, 100, 100]
    box2 = [0, 0, 100, 100]
    iou = calculate_iou(box1, box2)
    assert iou == pytest.approx(1.0)
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_inference.py

# Run with coverage
pytest --cov=src/screw_detector --cov-report=html

# Run only fast tests
pytest -m "not slow"
```

### Test Coverage

- Aim for >80% code coverage
- New features should have >90% coverage
- Critical paths should have 100% coverage

## Submitting Changes

### Pull Request Process

1. **Update your branch**

   ```bash
   git fetch origin
   git rebase origin/develop
   ```

2. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**

   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Fill in the PR template

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow conventional format
- [ ] PR description clearly describes changes
- [ ] Linked to relevant issue (if applicable)

### Review Process

1. Automated checks (CI) must pass
2. At least one maintainer approval required
3. Address all review comments
4. Update PR as needed until approved

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions or share ideas
- **Email**: 3bsalam0@gmail.com

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to Screw Detector!
