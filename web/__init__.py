"""
Web Module - Self-contained web interface functionality

This module contains everything web interface-related:
- Modern HTML interface with beautiful styling
- JavaScript application for API interaction
- Configuration for frontend behavior
- Clean interface for other modules
- Comprehensive tests

Other modules should import from here:
    from web import web_service
"""

from .interface import web_service

# Import the app for Render deployment (since Render is using 'uvicorn web:app')
try:
    import sys
    import os
    # Add parent directory to path so we can import from develop
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from develop.app import create_app
    
    # Create the app instance that Render expects
    app = create_app()
    print("✅ FastAPI app created successfully for deployment")
except Exception as e:
    print(f"⚠️ Could not create FastAPI app: {e}")
    app = None

# Export the main service and app
__all__ = ['web_service', 'app']

print("✅ Web module loaded successfully")
