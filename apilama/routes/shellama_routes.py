#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SheLLama API Routes

This module provides Flask routes for interacting with the SheLLama service.
"""

import os
import sys
import importlib.util
from flask import Blueprint, request, jsonify, current_app
from apilama.logger import logger

# Create a blueprint for SheLLama routes
shellama_routes = Blueprint('shellama_routes', __name__)

# Try to import SheLLama modules
try:
    # Add shellama package to the path if needed
    shellama_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shellama'))
    if shellama_path not in sys.path:
        sys.path.append(shellama_path)
    
    # Import SheLLama modules
    from shellama import file_ops, dir_ops, shell, git_ops
    SHELLAMA_AVAILABLE = True
except ImportError as e:
    logger.error(f'Error importing SheLLama modules: {str(e)}')
    SHELLAMA_AVAILABLE = False


@shellama_routes.route('/api/shellama/health', methods=['GET'])
def health_check():
    """Health check endpoint for SheLLama service.
    
    Returns:
        JSON response with the status of the SheLLama service
    """
    logger.info('SheLLama health check')
    
    return jsonify({
        'status': 'ok' if SHELLAMA_AVAILABLE else 'error',
        'service': 'shellama',
        'available': SHELLAMA_AVAILABLE
    })


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
        # Get the list of files
        files = file_ops.list_files(directory, pattern)
        
        return jsonify({
            'status': 'success',
            'files': files
        })
    except Exception as e:
        logger.error(f'Error listing files in directory {directory}: {str(e)}')
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
