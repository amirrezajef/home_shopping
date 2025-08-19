from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize extensions
db = SQLAlchemy()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Enable CORS for React frontend
    CORS(app)
    
    # Register blueprints
    from api.routes.categories import categories_bp
    from api.routes.items import items_bp
    from api.routes.options import options_bp
    from api.routes.dashboard import dashboard_bp
    from api.routes.export import export_bp
    from api.routes.health import health_bp
    
    app.register_blueprint(categories_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(options_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(health_bp)
    
    return app