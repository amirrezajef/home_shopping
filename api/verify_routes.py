#!/usr/bin/env python3
"""
Script to verify that all routes are properly registered
"""

import sys
import os

# Add the parent directory to the path so we can import from api package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.app_factory import create_app

def verify_routes():
    app = create_app()
    with app.app_context():
        print("Verifying registered routes...")
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': str(rule)
            })
        
        # Sort routes by rule
        routes.sort(key=lambda x: x['rule'])
        
        print("Found {} routes:".format(len(routes)))
        for route in routes:
            print("  {} -> {} {}".format(route['rule'], route['endpoint'], route['methods']))

if __name__ == "__main__":
    verify_routes()