from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint('health', __name__, url_prefix='/api')

@health_bp.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "home-shopping-api"
    }), 200