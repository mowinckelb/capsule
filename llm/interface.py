"""
LLM Module Interface - Clean abstraction layer for other modules

This is what other modules import to interact with LLM functionality.
"""

from llm import LLMHandler

class LLMService:
    """
    LLM service that provides a clean interface to other modules
    """
    def __init__(self):
        self.llm_handler = LLMHandler()
    
    def process_input(self, user_id: str, input_text, is_query: bool = False, db_provider: str = None):
        """Process input through the LLM"""
        return self.llm_handler.process_input(user_id, input_text, is_query, db_provider)
    
    def get_provider(self):
        """Get the LLM provider name"""
        return self.llm_handler.provider
    
    def health_check(self):
        """Check if LLM service is healthy"""
        try:
            # Try a simple test
            test_result = self.llm_handler.process_input("test", "health check", is_query=False)
            return True
        except Exception:
            return False

# Global service instance that other modules can import
llm_service = LLMService()
