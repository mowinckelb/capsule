"""
Web Integration File

This imports the web functionality from the web module.
Other parts of the application import from here.
"""

import sys
import os

# Add the web module to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'web'))

from interface import web_service

# Export for backward compatibility with existing code
__all__ = ['web_service']

print("✅ Web integration loaded")
