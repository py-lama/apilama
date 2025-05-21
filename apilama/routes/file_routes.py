from flask import Blueprint, jsonify, request, current_app
import os
import glob
from pathlib import Path

file_routes = Blueprint('file_routes', __name__)


@file_routes.route('/api/files', methods=['GET'])
def get_files():
    """List all markdown files in the markdown directory."""
    try:
        markdown_dir = os.environ.get('MARKDOWN_DIR', './markdown')
        if not os.path.exists(markdown_dir):
            os.makedirs(markdown_dir, exist_ok=True)
            
        # Get all markdown files
        markdown_files = []
        for file_path in glob.glob(os.path.join(markdown_dir, '*.md')):
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            last_modified = os.path.getmtime(file_path)
            markdown_files.append({
                'name': file_name,
                'path': file_path,
                'size': file_size,
                'last_modified': last_modified
            })
            
        # Log the operation
        current_app.logger.info(f"Listed {len(markdown_files)} markdown files")
        
        return jsonify({
            'status': 'success',
            'files': markdown_files
        })
    except Exception as e:
        current_app.logger.error(f"Error listing files: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@file_routes.route('/api/file', methods=['GET'])
def get_file():
    """Get the content of a markdown file."""
    try:
        filename = request.args.get('filename')
        if not filename:
            return jsonify({
                'status': 'error',
                'message': 'Filename is required'
            }), 400
            
        markdown_dir = os.environ.get('MARKDOWN_DIR', './markdown')
        file_path = os.path.join(markdown_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                'status': 'error',
                'message': f'File {filename} not found'
            }), 404
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Log the operation
        current_app.logger.info(f"Read file {filename}")
        
        return jsonify({
            'status': 'success',
            'content': content
        })
    except Exception as e:
        current_app.logger.error(f"Error reading file: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@file_routes.route('/api/file', methods=['POST'])
def save_file():
    """Save content to a markdown file."""
    try:
        data = request.get_json()
        filename = data.get('filename')
        content = data.get('content')
        
        if not filename or content is None:
            return jsonify({
                'status': 'error',
                'message': 'Filename and content are required'
            }), 400
            
        markdown_dir = os.environ.get('MARKDOWN_DIR', './markdown')
        if not os.path.exists(markdown_dir):
            os.makedirs(markdown_dir, exist_ok=True)
            
        file_path = os.path.join(markdown_dir, filename)
        
        with open(file_path, 'w') as f:
            f.write(content)
            
        # Log the operation
        current_app.logger.info(f"Saved file {filename}")
        
        return jsonify({
            'status': 'success',
            'message': f'File {filename} saved successfully'
        })
    except Exception as e:
        current_app.logger.error(f"Error saving file: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@file_routes.route('/api/file', methods=['DELETE'])
def delete_file():
    """Delete a markdown file."""
    try:
        filename = request.args.get('filename')
        if not filename:
            return jsonify({
                'status': 'error',
                'message': 'Filename is required'
            }), 400
            
        markdown_dir = os.environ.get('MARKDOWN_DIR', './markdown')
        file_path = os.path.join(markdown_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                'status': 'error',
                'message': f'File {filename} not found'
            }), 404
            
        os.remove(file_path)
        
        # Log the operation
        current_app.logger.info(f"Deleted file {filename}")
        
        return jsonify({
            'status': 'success',
            'message': f'File {filename} deleted successfully'
        })
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
