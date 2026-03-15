"""
API key authentication decorator
"""
import os
from functools import wraps
from flask import request, jsonify


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = os.environ.get("API_KEY")

        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key not configured on server'
            }), 500

        client_key = request.headers.get("X-API-Key")

        if not client_key or client_key != api_key:
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 401

        return f(*args, **kwargs)
    return decorated
