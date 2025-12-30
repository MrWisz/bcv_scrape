from flask import Flask
from flasgger import Swagger
from app.config import swagger_config, swagger_template


def create_app():
    """
    Application factory pattern
    """
    app = Flask(__name__)

    # Initialize Swagger
    Swagger(app, config=swagger_config, template=swagger_template)

    # Register blueprints
    from app.routes.rates import rates_bp
    from app.routes.p2p import p2p_bp
    from app.routes.home import home_bp
    from app.routes.calculator import calculator_bp

    app.register_blueprint(rates_bp)
    app.register_blueprint(p2p_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(calculator_bp)

    return app
