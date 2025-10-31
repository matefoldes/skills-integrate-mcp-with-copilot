# Development Guide

This document describes the development setup, testing, and code quality tools for the Mergington High School API.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

The project uses pytest for testing. All tests are located in the `tests/` directory.

### Run all tests:
```bash
pytest
```

### Run tests with coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

### Run specific test file:
```bash
pytest tests/test_api.py
```

### Run tests verbosely:
```bash
pytest -v
```

## Code Quality

### Formatting with Black

Black is used for consistent code formatting:

```bash
# Check formatting
black --check src/ tests/

# Auto-format code
black src/ tests/
```

### Linting with Ruff

Ruff is used for fast Python linting:

```bash
# Check for issues
ruff check src/ tests/

# Auto-fix issues
ruff check src/ tests/ --fix
```

## Pre-commit Hooks

Pre-commit hooks are configured to run automatically before each commit. They check:
- Code formatting (black)
- Linting (ruff)
- Common issues (trailing whitespace, large files, etc.)

### Install pre-commit hooks:
```bash
pre-commit install
```

### Run pre-commit manually:
```bash
pre-commit run --all-files
```

## Continuous Integration

A GitHub Actions workflow (`.github/workflows/tests.yml`) runs automatically on:
- Push to `main` or `copilot/**` branches
- Pull requests to `main`

The CI workflow:
1. Runs all tests with coverage reporting
2. Checks code formatting with black
3. Runs linting with ruff

## Test Coverage

Current test coverage: **97%**

Tests cover:
- API endpoints (GET /activities, POST signup, DELETE unregister)
- Database initialization and seeding
- Activity and Participant models
- Error handling (404s, 400s)
- Edge cases (capacity limits, duplicate signups, etc.)
