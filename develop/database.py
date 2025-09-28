"""
Database Integration File

This imports the database functionality from the database module.
Other parts of the application import from here.
"""

import sys
import os

# Add the database module to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database'))

from interface import database_service
from database import DBHandler

# Export for backward compatibility with existing code
__all__ = ['database_service', 'DBHandler']

print("✅ Database integration loaded")
