import sys
import os
# Add the parent directory to the path so we can import from api package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.app_factory import create_app

app = create_app()

if __name__ == '__main__':
    # Get host and port from environment variables or use defaults
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host=host, port=port, debug=False)