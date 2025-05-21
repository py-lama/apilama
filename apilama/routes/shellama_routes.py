#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SheLLama API Routes

This module provides Flask routes for interacting with the SheLLama service.
"""

from flask import Blueprint, request, jsonify, current_app
from apilama.logger import logger

# Create a blueprint for SheLLama routes
shellama_routes = Blueprint('shellama_routes', __name__)


@shellama_routes.route('/api/shellama/health', methods=['GET'])
def health_check():
    """Health check endpoint for SheLLama service.
    
    Returns:
        JSON response with the status of the SheLLama service
    """
    logger.info('SheLLama health check')
    
    # TODO: Implement actual health check for SheLLama service
    return jsonify({
        'status': 'ok',
        'service': 'shellama'
    })


@shellama_routes.route('/api/shellama/files', methods=['GET'])
def get_files():
    """Get a list of files from the filesystem.
    
    Returns:
        JSON response with a list of files
    """
    # Get the directory path from the query parameters
    directory = request.args.get('directory', '.')
    
    logger.info(f'Listing files in directory: {directory}')
    
    # TODO: Implement actual file listing with SheLLama
    # This is a placeholder for the actual implementation
    result = {
        'status': 'success',
        'files': [
            {
                'name': 'example.md',
                'path': f'{directory}/example.md',
                'size': 1024,
                'modified': 1620000000.0
            },
            {
                'name': 'sample.md',
                'path': f'{directory}/sample.md',
                'size': 2048,
                'modified': 1620100000.0
            }
        ]
    }
    
    return jsonify(result)


@shellama_routes.route('/api/shellama/file', methods=['GET'])
def get_file_content():
    """Get the content of a file.
    
    Returns:
        JSON response with the file content
    """
    # Get the filename from the query parameters
    filename = request.args.get('filename')
    
    if not filename:
        logger.error('Invalid request: No filename provided')
        return jsonify({
            'status': 'error',
            'message': 'No filename provided'
        }), 400
    
    logger.info(f'Getting content of file: {filename}')
    
    # TODO: Implement actual file reading with SheLLama
    # This is a placeholder for the actual implementation
    result = {
        'status': 'success',
        'content': f'Content of file {filename}',
        'name': filename.split('/')[-1]
    }
    
    return jsonify(result)


@shellama_routes.route('/api/shellama/file', methods=['POST'])
def create_file():
    """Create or update a file.
    
    Returns:
        JSON response with the result
    """
    data = request.get_json()
    
    if not data or 'path' not in data or 'content' not in data:
        logger.error('Invalid request: Missing required fields')
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields (path, content)'
        }), 400
    
    path = data['path']
    content = data['content']
    commit_message = data.get('commit_message', 'Update file')
    
    logger.info(f'Creating/updating file: {path}')
    
    # TODO: Implement actual file writing with SheLLama
    # This is a placeholder for the actual implementation
    result = {
        'status': 'success',
        'message': f'File {path} created/updated successfully',
        'path': path
    }
    
    return jsonify(result)
