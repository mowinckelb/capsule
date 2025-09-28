"""
Frontend Integration File

This imports the frontend functionality from the frontend module.
Other parts of the application import from here.
"""

import sys
import os

# Add the frontend module to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend'))

from frontend.interface import frontend_service

# Export for backward compatibility with existing code
__all__ = ['frontend_service']

print("✅ Frontend integration loaded")
