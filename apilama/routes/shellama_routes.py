#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SheLLama API Routes

This module provides Flask routes for interacting with the SheLLama service.
It proxies requests to the SheLLama REST API service.
"""

import os
import requests
import json
from flask import Blueprint, request, jsonify, current_app
from apilama.logger import logger

# Create a blueprint for SheLLama routes
shellama_routes = Blueprint('shellama_routes', __name__)

# Get SheLLama service URL from environment variable or use default
SHELLAMA_API_URL = os.environ.get('SHELLAMA_API_URL', 'http://localhost:8002')

# Function to check if SheLLama service is available
def is_shellama_available():
    try:
        response = requests.get(f"{SHELLAMA_API_URL}/health", timeout=2)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error connecting to SheLLama service: {str(e)}")
        return False

# Check if SheLLama service is available
SHELLAMA_AVAILABLE = is_shellama_available()


@shellama_routes.route('/api/shellama/health', methods=['GET'])
def health_check():
    """Health check endpoint for SheLLama service.
    
    Returns:
        JSON response with the status of the SheLLama service
    """
    logger.info('SheLLama health check')
    
    try:
        # Forward the request to the SheLLama service
        response = requests.get(f"{SHELLAMA_API_URL}/health", timeout=5)
        
        if response.status_code == 200:
            # Return the SheLLama service response
            shellama_response = response.json()
            return jsonify({
                'status': 'ok',
                'service': 'shellama',
                'available': True,
                'details': shellama_response
            })
        else:
            # Return error if SheLLama service returns non-200 status code
            return jsonify({
                'status': 'error',
                'service': 'shellama',
                'available': False,
                'message': f"SheLLama service returned status code {response.status_code}"
            }), 502
    except Exception as e:
        # Return error if SheLLama service is unavailable
        logger.error(f"Error connecting to SheLLama service: {str(e)}")
        return jsonify({
            'status': 'error',
            'service': 'shellama',
            'available': False,
            'message': f"Error connecting to SheLLama service: {str(e)}"
        }), 502


@shellama_routes.route('/api/shellama/files', methods=['GET'])
def get_files():
    """Get a list of files from the filesystem.
    
    Returns:
        JSON response with a list of files
    """
    # Check if SheLLama is available
    if not SHELLAMA_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'SheLLama service is not available'
        }), 503
    
    # Get the directory path and pattern from the query parameters
    directory = request.args.get('directory', '.')
    pattern = request.args.get('pattern', '*.*')
    
    logger.info(f'Listing files in directory: {directory} with pattern: {pattern}')
    
    try:
        # Forward the request to the SheLLama service
        response = requests.get(
            f"{SHELLAMA_API_URL}/files",
            params={'directory': directory, 'pattern': pattern},
            timeout=10
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the SheLLama service response
            return jsonify(response.json())
        else:
            # Return error if SheLLama service returns non-200 status code
            error_message = f"SheLLama service returned status code {response.status_code}"
            logger.error(error_message)
            return jsonify({
                'status': 'error',
                'message': error_message
            }), 502
    except Exception as e:
        logger.error(f'Error listing files: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@shellama_routes.route('/api/shellama/file', methods=['GET'])
def get_file_content():
    """Get the content of a file.
    
    Returns:
        JSON response with the file content
    """
    # Check if SheLLama is available
    if not SHELLAMA_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'SheLLama service is not available'
        }), 503
    
    # Get the filename from the query parameters
    filename = request.args.get('filename')
    
    if not filename:
        logger.error('Invalid request: No filename provided')
        return jsonify({
            'status': 'error',
            'message': 'No filename provided'
        }), 400
    
    logger.info(f'Getting content of file: {filename}')
    
    try:
        # Read the file content
        content = file_ops.read_file(filename)
        
        return jsonify({
            'status': 'success',
            'content': content,
            'name': os.path.basename(filename)
        })
    except FileNotFoundError:
        logger.error(f'File not found: {filename}')
        return jsonify({
            'status': 'error',
            'message': f'File not found: {filename}'
        }), 404
    except Exception as e:
        logger.error(f'Error reading file {filename}: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@shellama_routes.route('/api/shellama/file', methods=['POST'])
def create_file():
    """Create or update a file.
    
    Returns:
        JSON response with the result
    """
    # Check if SheLLama is available
    if not SHELLAMA_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'SheLLama service is not available'
        }), 503
    
    data = request.get_json()
    
    if not data or 'path' not in data or 'content' not in data:
        logger.error('Invalid request: Missing required fields')
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields (path, content)'
        }), 400
    
    path = data['path']
    content = data['content']
    
    logger.info(f'Creating/updating file: {path}')
    
    try:
        # Write the file content
        file_ops.write_file(path, content)
        
        return jsonify({
            'status': 'success',
            'message': f'File {path} created/updated successfully',
            'path': path
        })
    except Exception as e:
        logger.error(f'Error writing file {path}: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@shellama_routes.route('/api/shellama/file', methods=['DELETE'])
def delete_file():
    """Delete a file.
    
    Returns:
        JSON response with the result
    """
    # Check if SheLLama is available
    if not SHELLAMA_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'SheLLama service is not available'
        }), 503
    
    # Get the filename from the query parameters
    filename = request.args.get('filename')
    
    if not filename:
        logger.error('Invalid request: No filename provided')
        return jsonify({
            'status': 'error',
            'message': 'No filename provided'
        }), 400
    
    logger.info(f'Deleting file: {filename}')
    
    try:
        # Delete the file
        file_ops.delete_file(filename)
        
        return jsonify({
            'status': 'success',
            'message': f'File {filename} deleted successfully'
        })
    except FileNotFoundError:
        logger.error(f'File not found: {filename}')
        return jsonify({
            'status': 'error',
            'message': f'File not found: {filename}'
        }), 404
    except Exception as e:
        logger.error(f'Error deleting file {filename}: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@shellama_routes.route('/api/shellama/directory', methods=['GET'])
def get_directories():
    """Get a list of directories in a parent directory.
    
    Returns:
        JSON response with a list of directories
    """
    # Check if SheLLama is available
    if not SHELLAMA_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'SheLLama service is not available'
        }), 503
    
    # Get the directory path from the query parameters
    directory = request.args.get('directory', '.')
    
    logger.info(f'Listing directories in: {directory}')
    
    try:
        # Get the list of directories
        directories = dir_ops.list_directories(directory)
        
        return jsonify({
            'status': 'success',
            'directories': directories
        })
    except FileNotFoundError:
        logger.error(f'Directory not found: {directory}')
        return jsonify({
            'status': 'error',
            'message': f'Directory not found: {directory}'
        }), 404
    except Exception as e:
        logger.error(f'Error listing directories in {directory}: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@shellama_routes.route('/api/shellama/directory', methods=['POST'])
def create_directory():
    """Create a directory.
    
    Returns:
        JSON response with the result
    """
    # Check if SheLLama is available
    if not SHELLAMA_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'SheLLama service is not available'
        }), 503
    
    data = request.get_json()
    
    if not data or 'path' not in data:
        logger.error('Invalid request: Missing required fields')
        return jsonify({
            'status': 'error',
            'message': 'Missing required field (path)'
        }), 400
    
    path = data['path']
    
    logger.info(f'Creating directory: {path}')
    
    try:
        # Create the directory
        dir_ops.create_directory(path)
        
        return jsonify({
            'status': 'success',
            'message': f'Directory {path} created successfully',
            'path': path
        })
    except Exception as e:
        logger.error(f'Error creating directory {path}: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@shellama_routes.route('/api/shellama/directory', methods=['DELETE'])
def delete_directory():
    """Delete a directory.
    
    Returns:
        JSON response with the result
    """
    # Check if SheLLama is available
    if not SHELLAMA_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'SheLLama service is not available'
        }), 503
    
    # Get the directory path and recursive flag from the query parameters
    directory = request.args.get('directory')
    recursive = request.args.get('recursive', 'false').lower() == 'true'
    
    if not directory:
        logger.error('Invalid request: No directory provided')
        return jsonify({
            'status': 'error',
            'message': 'No directory provided'
        }), 400
    
    logger.info(f'Deleting directory: {directory} (recursive={recursive})')
    
    try:
        # Delete the directory
        dir_ops.delete_directory(directory, recursive)
        
        return jsonify({
            'status': 'success',
            'message': f'Directory {directory} deleted successfully'
        })
    except FileNotFoundError:
        logger.error(f'Directory not found: {directory}')
        return jsonify({
            'status': 'error',
            'message': f'Directory not found: {directory}'
        }), 404
    except Exception as e:
        logger.error(f'Error deleting directory {directory}: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@shellama_routes.route('/api/shellama/shell', methods=['POST'])
def execute_shell_command():
    """Execute a shell command.
    
    Returns:
        JSON response with the command execution result
    """
    # Check if SheLLama is available
    if not SHELLAMA_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'SheLLama service is not available'
        }), 503
    
    data = request.get_json()
    
    if not data or 'command' not in data:
        logger.error('Invalid request: Missing required fields')
        return jsonify({
            'status': 'error',
            'message': 'Missing required field (command)'
        }), 400
    
    command = data['command']
    cwd = data.get('cwd')
    timeout = data.get('timeout')
    use_shell = data.get('shell', False)
    
    logger.info(f'Executing shell command: {command}')
    
    try:
        # Execute the command
        result = shell.execute_command(
            command,
            cwd=cwd,
            timeout=timeout,
            shell=use_shell
        )
        
        return jsonify({
            'status': 'success' if result['success'] else 'error',
            'exit_code': result['exit_code'],
            'stdout': result['stdout'],
            'stderr': result['stderr'],
            'execution_time': result['execution_time']
        })
    except Exception as e:
        logger.error(f'Error executing shell command {command}: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
