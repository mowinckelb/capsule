"""
Authentication Integration File

This imports the authentication functionality from the authentication module.
Other parts of the application import from here.
"""

import sys
import os

# Add the authentication module to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'authentication'))

from interface import auth_service
from auth import AuthHandler

# Export for backward compatibility with existing code
__all__ = ['auth_service', 'AuthHandler']

print("✅ Authentication integration loaded")
