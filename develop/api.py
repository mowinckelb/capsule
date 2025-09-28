"""
API Integration File

This imports the API functionality from the API module.
Other parts of the application import from here.
"""

import sys
import os

# Add the API module to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api'))

from interface import api_service
from server import create_app, start_server
from routes import api_routes

# Export for backward compatibility with existing code
__all__ = ['api_service', 'create_app', 'start_server', 'api_routes']

print("✅ API integration loaded")
