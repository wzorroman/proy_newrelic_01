from flask import Flask
from dotenv import load_dotenv
import os
import newrelic.agent

def create_app():
    """Factory function to create Flask application"""
    load_dotenv()
    
    # Initialize NewRelic
    newrelic.agent.initialize()
    
    app = Flask(__name__)
    
    # Basic configuration
    app.config.from_object('app.config.config.Config')
    
    # Register blueprints/controllers
    from app.controllers.api_controller import api_bp
    app.register_blueprint(api_bp)
    
    # Initialize database
    from app.models.database import init_db
    init_db(app)
    
    return app
