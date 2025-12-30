"""
Routes for calculator web app
"""
from flask import Blueprint, render_template

calculator_bp = Blueprint('calculator', __name__)


@calculator_bp.route('/calculator', methods=['GET'])
def calculator():
    """
    Telegram Web App - Currency Calculator
    Renders an interactive calculator for converting USD/EUR to VES
    """
    return render_template('calculator.html')
