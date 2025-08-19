#!/usr/bin/env python3
"""
Script to verify that all modules can be imported correctly
"""

import sys
import os

# Add the parent directory to the path so we can import from api package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    print("Testing imports...")
    
    try:
        from api.app_factory import create_app, db
        print("SUCCESS: app_factory imported successfully")
    except Exception as e:
        print("ERROR: Failed to import app_factory: {}".format(e))
        return False
    
    try:
        from api.models import Category, Subcategory, Item, Option
        print("SUCCESS: models imported successfully")
    except Exception as e:
        print("ERROR: Failed to import models: {}".format(e))
        return False
    
    try:
        from api.utils.helpers import ensure_one_selected
        print("SUCCESS: utils imported successfully")
    except Exception as e:
        print("ERROR: Failed to import utils: {}".format(e))
        return False
    
    try:
        from api.routes.categories import categories_bp
        from api.routes.items import items_bp
        from api.routes.options import options_bp
        from api.routes.dashboard import dashboard_bp
        from api.routes.export import export_bp
        from api.routes.health import health_bp
        print("SUCCESS: routes imported successfully")
    except Exception as e:
        print("ERROR: Failed to import routes: {}".format(e))
        return False
    
    print("SUCCESS: All imports successful!")
    return True

if __name__ == "__main__":
    success = test_imports()
    if not success:
        sys.exit(1)