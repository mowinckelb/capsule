"""
Authentication Module - Self-contained authentication functionality

This module contains everything authentication-related:
- Complete user registration and login system
- Password hashing and verification
- Token-based authentication
- Clean interface for other modules
- Comprehensive tests

Other modules should import from here:
    from authentication import auth_service
"""

from .interface import auth_service

# Export the main service
__all__ = ['auth_service']

print("✅ Authentication module loaded successfully")
