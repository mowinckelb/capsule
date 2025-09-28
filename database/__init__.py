"""
Database Module - Self-contained database functionality

This module contains everything database-related:
- Original database.py implementation
- Clean interface for other modules  
- Comprehensive tests
- Configuration

Other modules should import from here:
    from database_module import database_service
"""

from .interface import database_service

# Export the main service
__all__ = ['database_service']

print("✅ Database module loaded successfully")
