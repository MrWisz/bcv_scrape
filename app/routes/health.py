"""
Health check endpoint to keep the server awake
"""
from flask import Blueprint, jsonify
from app.extensions import limiter
from app.config import RATE_LIMIT_HEALTH

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
@limiter.limit(RATE_LIMIT_HEALTH)
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
