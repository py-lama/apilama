FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the package files
COPY . .

# Install the package in development mode
RUN pip install -e .

# Expose the API port
EXPOSE 8080

# Environment variables
ENV PORT=8080
ENV HOST=0.0.0.0
ENV DEBUG=False

# Command to run the API server
CMD ["python", "-m", "apilama.app", "--port", "8080", "--host", "0.0.0.0"]
