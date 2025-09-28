"""
LLM Module

This module provides LLM functionality through a clean interface.
Other modules should only import from here.
"""

from .interface import llm_service
from .grok_implementation import GrokLLMImplementation

# Initialize the LLM service with Grok implementation
try:
    grok_impl = GrokLLMImplementation()
    llm_service.initialize(grok_impl)
    print("✓ LLM Module initialized with Grok")
except Exception as e:
    print(f"✗ LLM Module initialization failed: {e}")

# Export the service for other modules to use
__all__ = ['llm_service']
