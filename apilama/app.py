#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
APILama - Main application module

This module provides the Flask application for the APILama service.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Handle different ways the dotenv package might be installed
try:
    from dotenv import load_dotenv
except ImportError:
    try:
        from python_dotenv import load_dotenv
    except ImportError:
        # If dotenv is not available, define a dummy function
        def load_dotenv(path=None):
            logging.warning("python-dotenv package not found, environment variables from .env will not be loaded")
            pass

from flask import Flask, jsonify

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

# Import custom logger
from apilama.logger import logger, init_app

# Add the parent directory to sys.path to import pylama modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import blueprints
from apilama.routes.pylama_routes import pylama_routes
from apilama.routes.pybox_routes import pybox_routes
from apilama.routes.pyllm_routes import pyllm_routes
from apilama.routes.shellama_routes import shellama_routes


def create_app(test_config=None):
    """Create and configure the Flask application.
    
    Args:
        test_config (dict, optional): Test configuration to override default config.
        
    Returns:
        Flask: The configured Flask application.
    """
    # Create and configure the app
    app = Flask(__name__)
    
    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DEBUG=os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't'),
    )
    
    # Override with test config if provided
    if test_config is not None:
        app.config.update(test_config)
    
    # Initialize the logger
    init_app(app)
    
    # Register blueprints
    app.register_blueprint(pylama_routes)
    app.register_blueprint(pybox_routes)
    app.register_blueprint(pyllm_routes)
    app.register_blueprint(shellama_routes)
    
    # Add a health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'ok', 'service': 'apilama'})
    
    # Log the initialization
    logger.info(f"APILama initialized")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    
    return app


def main():
    """Run the Flask application.
    
    This function is the entry point for the application when run directly.
    Supports both environment variables and command-line arguments.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='APILama - Backend API service for the PyLama ecosystem')
    parser.add_argument('--port', type=int, default=int(os.environ.get('PORT', 8000)),
                        help='Port to run the server on (default: 8000)')
    parser.add_argument('--host', type=str, default=os.environ.get('HOST', '127.0.0.1'),
                        help='Host to run the server on (default: 127.0.0.1)')
    parser.add_argument('--debug', action='store_true', default=None,
                        help='Run in debug mode')
    args = parser.parse_args()
    
    # Set environment variables from arguments
    if args.debug is not None:
        os.environ['DEBUG'] = str(args.debug)
    
    # Create the app
    app = create_app()
    
    # Print startup message
    print(f"Starting APILama on {args.host}:{args.port} (debug={app.config['DEBUG']})")
    
    # Run the app
    app.run(host=args.host, port=args.port, debug=app.config['DEBUG'])


if __name__ == '__main__':
    main()
