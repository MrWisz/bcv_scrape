"""
Routes for calculator web app
"""
from flask import Blueprint, render_template
from app.auth import require_api_key

calculator_bp = Blueprint('calculator', __name__)


@calculator_bp.route('/calculator', methods=['GET'])
@require_api_key
def calculator():
    """
    Telegram Web App - Currency Calculator
    Renders an interactive calculator for converting USD/EUR to VES
    """
    return render_template('calculator.html')
