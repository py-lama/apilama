# APILama

APILama is the API gateway for the PyLama ecosystem. It serves as the central communication layer between the frontend WebLama interface and the various backend services (PyLama, PyBox, PyLLM, SheLLama).

## Features

- **Unified API Gateway**: Single entry point for all PyLama ecosystem services
- **Service Routing**: Intelligent routing of requests to appropriate backend services (PyBox, PyLLM, SheLLama, PyLama)
- **RESTful API Design**: Clean and consistent API endpoints for all operations
- **Cross-Origin Resource Sharing (CORS)**: Support for cross-origin requests from the WebLama frontend
- **Authentication and Authorization**: Secure access to API endpoints
- **Response Standardization**: Consistent response format across all services
- **Error Handling**: Comprehensive error handling and reporting
- **Logging and Monitoring**: Detailed logging of requests and responses for debugging and monitoring

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
