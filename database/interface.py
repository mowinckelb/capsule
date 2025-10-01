"""
Database Module Interface - Clean abstraction layer for other modules

This is what other modules import to interact with database functionality.
"""

import logging
from typing import Union, List, Dict, Any
from .database import DBHandler

logger = logging.getLogger(__name__)

class DatabaseService:
    """
    Database service that provides a clean interface to other modules
    """
    def __init__(self):
        self.db_handler = DBHandler()
    
    def add_memory(self, user_id: str, memory: Union[str, Dict[str, Any]]) -> None:
        """Add a memory for a user"""
        try:
            return self.db_handler.add_memory(user_id, memory)
        except Exception as e:
            logger.error(f"Failed to add memory for user {user_id}: {e}")
            raise
    
    def query_memories(self, user_id: str, query: Union[str, Dict[str, Any]], top_k: int = 5) -> List[str]:
        """Query memories for a user"""
        try:
            return self.db_handler.query_memories(user_id, query, top_k)
        except Exception as e:
            logger.error(f"Failed to query memories for user {user_id}: {e}")
            raise
    
    def get_provider(self) -> str:
        """Get the database provider name"""
        return self.db_handler.provider
    
    def health_check(self) -> bool:
        """Check if database is healthy"""
        try:
            self.db_handler.get_index()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

# Global service instance that other modules can import
database_service = DatabaseService()
