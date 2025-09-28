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

from interface import web_service

# Export the main service
__all__ = ['web_service']

print("✅ Web module loaded successfully")
