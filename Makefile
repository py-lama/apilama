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

.PHONY: all setup venv clean test lint format run run-port

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
