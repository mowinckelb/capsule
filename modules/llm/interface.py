"""
LLM Module Interface - Abstraction Layer

This is the ONLY interface other modules should use to interact with LLM functionality.
All LLM-related operations go through this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Union


class LLMInterface(ABC):
    """Abstract interface for LLM operations"""
    
    @abstractmethod
    def process_input(self, user_id: str, input_text: Union[str, Dict[str, Any]], 
                     is_query: bool = False, context: str = None) -> Union[str, Dict[str, Any]]:
        """
        Process user input through LLM
        
        Args:
            user_id: User identifier
            input_text: Text or structured input to process
            is_query: Whether this is a query (True) or storage (False)
            context: Additional context for processing
            
        Returns:
            Processed response (string for queries, dict for storage)
        """
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """Check if LLM service is healthy"""
        pass
    
    @abstractmethod
    def get_provider_info(self) -> Dict[str, str]:
        """Get information about the LLM provider"""
        pass


class LLMService:
    """
    Main LLM Service - This is what other modules import
    Singleton pattern to ensure consistent interface
    """
    _instance = None
    _llm_implementation = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self, llm_implementation: LLMInterface):
        """Initialize with specific LLM implementation"""
        self._llm_implementation = llm_implementation
    
    def process_input(self, user_id: str, input_text: Union[str, Dict[str, Any]], 
                     is_query: bool = False, context: str = None) -> Union[str, Dict[str, Any]]:
        """Process input through the LLM"""
        if not self._llm_implementation:
            raise RuntimeError("LLM service not initialized")
        return self._llm_implementation.process_input(user_id, input_text, is_query, context)
    
    def health_check(self) -> bool:
        """Check LLM health"""
        if not self._llm_implementation:
            return False
        return self._llm_implementation.health_check()
    
    def get_info(self) -> Dict[str, str]:
        """Get LLM provider info"""
        if not self._llm_implementation:
            return {"status": "not_initialized"}
        return self._llm_implementation.get_provider_info()


# Global instance that other modules will import
llm_service = LLMService()
