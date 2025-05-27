# APILama Makefile

# Default port for the API server
PORT ?= 8000
HOST ?= 127.0.0.1

# Python virtual environment
VENV := venv
PYTHON := python3
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
BLACK := $(VENV)/bin/black
FLAKE8 := $(VENV)/bin/flake8

.PHONY: all setup venv clean test lint format run run-port docker-test docker-build docker-clean docker-integration docker-mock test-package update-version publish publish-test

all: setup

# Create virtual environment and install dependencies
venv:
	$(PYTHON) -m venv $(VENV)

setup: venv
	$(PIP) install -e .
	$(PIP) install -e ".[dev]"

# Run tests
test: setup
	$(PYTEST) tests/

# Lint code
lint: setup
	$(FLAKE8) apilama/ tests/

# Format code
format: setup
	$(BLACK) apilama/ tests/

# Run the API server
run: setup
	$(VENV)/bin/python -m apilama.app --port $(PORT) --host $(HOST)

# Alias for run with PORT parameter for backward compatibility
run-port: run

# Clean up
clean:
	rm -rf $(VENV) *.egg-info build/ dist/ __pycache__/ .pytest_cache/ .coverage

# Docker testing targets
docker-build:
	@echo "Building Docker test images..."
	@./run_docker_tests.sh --build

docker-test: docker-build
	@echo "Running tests in Docker..."
	@./run_docker_tests.sh --run-tests

docker-integration: docker-build
	@echo "Running integration tests in Docker..."
	@./run_docker_tests.sh --integration

docker-mock: docker-build
	@echo "Starting APILama mock service in Docker..."
	@./run_docker_tests.sh --mock-service

docker-interactive: docker-build
	@echo "Starting interactive Docker test environment..."
	@./run_docker_tests.sh --interactive

docker-clean:
	@echo "Cleaning Docker test environment..."
	@./run_docker_tests.sh --clean


# Build package
build: setup
	@echo "Building package..."
	@. venv/bin/activate && rm -rf dist/* && python setup.py sdist bdist_wheel

# Test package
test-package: setup
	@echo "Testing package..."
	@. venv/bin/activate && pytest

# Update version
update-version:
	@echo "Updating package version..."
	@python ../scripts/update_version.py

# Publish package to PyPI
publish: test-package update-version build
	@echo "Publishing package to PyPI..."
	@. venv/bin/activate && twine check dist/* && twine upload dist/*

# Publish package to TestPyPI
publish-test: test-package update-version build
	@echo "Publishing package to TestPyPI..."
	@. venv/bin/activate && twine check dist/* && twine upload --repository testpypi dist/*
