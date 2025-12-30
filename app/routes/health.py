"""
Health check endpoint to keep the server awake
"""
from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - General
    summary: Health check endpoint
    description: Simple endpoint to verify the API is running. Used by monitoring services to keep the server awake.
    responses:
      200:
        description: API is healthy and running
        schema:
          type: object
          properties:
            status:
              type: string
              example: "ok"
    """
    return jsonify({'status': 'ok'}), 200
