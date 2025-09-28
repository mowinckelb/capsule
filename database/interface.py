"""
Database Module Interface - Clean abstraction layer for other modules

This is what other modules import to interact with database functionality.
"""

from database import DBHandler

class DatabaseService:
    """
    Database service that provides a clean interface to other modules
    """
    def __init__(self):
        self.db_handler = DBHandler()
    
    def add_memory(self, user_id: str, memory):
        """Add a memory for a user"""
        return self.db_handler.add_memory(user_id, memory)
    
    def query_memories(self, user_id: str, query, top_k: int = 5):
        """Query memories for a user"""
        return self.db_handler.query_memories(user_id, query)
    
    def get_provider(self):
        """Get the database provider name"""
        return self.db_handler.provider
    
    def health_check(self):
        """Check if database is healthy"""
        try:
            # Try a simple operation
            self.db_handler.get_index()
            return True
        except Exception:
            return False

# Global service instance that other modules can import
database_service = DatabaseService()
