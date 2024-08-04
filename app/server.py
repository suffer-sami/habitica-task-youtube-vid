from flask import Flask
import logging
from .webhook import webhook_bp

def create_app():
    app = Flask(__name__)
    
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    
    app.register_blueprint(webhook_bp)

    return app