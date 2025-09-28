"""
API Module - Self-contained API functionality

This module contains everything API-related:
- FastAPI routes and endpoints
- Server configuration and startup
- Dependency injection for other modules
- Clean interface for integration
- Comprehensive tests

Other modules should import from here:
    from api import api_service
"""

from .interface import api_service

# Export the main service
__all__ = ['api_service']

print("✅ API module loaded successfully")
