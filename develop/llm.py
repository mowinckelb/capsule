"""
LLM Integration File

This imports the LLM functionality from the LLM module.
Other parts of the application import from here.
"""

import sys
import os

# Add the LLM module to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'llm'))

from llm.interface import llm_service
from llm.llm import LLMHandler

# Export for backward compatibility with existing code
__all__ = ['llm_service', 'LLMHandler']

print("✅ LLM integration loaded")
