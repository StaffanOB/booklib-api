#!/usr/bin/env python3
"""
Development server runner for BookLib API.
This script loads environment variables and runs the Flask application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    from app import create_app
    
    # Print configuration info
    print("Starting BookLib API Development Server")
    print("=====================================")
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
    print(f"FLASK_ENV: {os.getenv('FLASK_ENV')}")
    print(f"DEBUG: {os.getenv('DEBUG')}")
    print("=====================================")
    
    # Create and run the app
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)