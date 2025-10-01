"""
LLM Module - Self-contained LLM functionality

This module contains everything LLM-related:
- Original llm.py implementation
- Clean interface for other modules  
- Comprehensive tests
- Configuration

Other modules should import from here:
    from llm import llm_service
"""

from .interface import llm_service

# Export the main service
__all__ = ['llm_service']

print("LLM module loaded successfully")
