"""
Flask application factory and entry point for the BookLib API.
This file provides the Flask application instance that can be discovered by the Flask CLI.
"""
import os
from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the development server
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    )