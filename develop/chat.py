"""
Chat Integration File

This imports the chat functionality from the chat module.
Other parts of the application import from here.
"""

import sys
import os

# Add the chat module to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chat'))

from chat.interface import chat_service
from chat.cli import CapsuleCLI

# Export for backward compatibility with existing code
__all__ = ['chat_service', 'CapsuleCLI']

def run_cli():
    """Run the CLI interface"""
    chat_service.run_cli()

if __name__ == "__main__":
    run_cli()

print("✅ Chat integration loaded")