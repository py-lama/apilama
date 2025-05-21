# APILama

APILama is the backend API service for the PyLama ecosystem. It serves as the communication layer between the frontend WebLama interface and the various backend services (PyLama, PyBox, PyLLM, SheLLama).

## Features

- RESTful API endpoints for all PyLama ecosystem services
- Authentication and authorization for API access
- Request routing to appropriate backend services
- Response formatting and standardization
- Error handling and logging

## Installation

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

```bash
# Start the API server
apilama run

# Or with custom port
apilama run --port 8000
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest

# Format code
black apilama tests

# Lint code
flake8 apilama tests
```

## License

MIT
