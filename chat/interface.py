"""
Chat Module Interface - Clean abstraction layer for other modules

This is what other modules import to interact with chat functionality.
"""

from .cli import CapsuleCLI
from .handlers import get_message_handler, ChatMessageHandler

class ChatService:
    """
    Chat service that provides a clean interface to other modules
    """
    
    def __init__(self):
        self.cli = None
        self.handlers = {}
    
    def get_cli_interface(self):
        """Get a CLI interface instance"""
        if not self.cli:
            self.cli = CapsuleCLI()
        return self.cli
    
    def run_cli(self):
        """Run the CLI interface"""
        cli = self.get_cli_interface()
        cli.run()
    
    def get_message_handler(self, interface_type: str = 'cli'):
        """Get a message handler for the specified interface"""
        if interface_type not in self.handlers:
            self.handlers[interface_type] = get_message_handler(interface_type)
        return self.handlers[interface_type]
    
    def parse_message(self, message: str, interface_type: str = 'cli'):
        """Parse a message using the appropriate handler"""
        handler = self.get_message_handler(interface_type)
        return handler.parse_message(message)
    
    def format_response(self, response, query: str = None, interface_type: str = 'cli'):
        """Format a response using the appropriate handler"""
        handler = self.get_message_handler(interface_type)
        return handler.format_response(response, query)
    
    def health_check(self):
        """Check if chat service is healthy"""
        try:
            # Test message parsing
            test_message = "input: test memory"
            handler = self.get_message_handler('cli')
            parsed = handler.parse_message(test_message)
            
            return {
                'healthy': True,
                'handlers_available': list(self.handlers.keys()),
                'test_parse_success': parsed['type'] == 'command'
            }
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }

# Global service instance that other modules can import
chat_service = ChatService()
