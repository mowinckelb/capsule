"""
API Server

This is the main server file that starts the FastAPI application.
It can be run independently to test just the API functionality.
"""

import uvicorn
import os
from config import API_CONFIG
from routes import api_routes

def create_app():
    """Create and configure the FastAPI application"""
    app = api_routes.get_app()
    
    # Add any additional app-level configuration here
    if API_CONFIG['debug']:
        print("🐛 Debug mode enabled")
    
    return app

def start_server():
    """Start the API server"""
    app = create_app()
    
    print(f"🚀 Starting Capsule API Server")
    print(f"📡 Host: {API_CONFIG['host']}")
    print(f"🔌 Port: {API_CONFIG['port']}")
    print(f"🔄 Reload: {API_CONFIG['reload']}")
    
    uvicorn.run(
        app,
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        reload=API_CONFIG['reload']
    )

if __name__ == "__main__":
    start_server()
