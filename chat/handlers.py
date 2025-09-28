"""
Chat Message Handlers

This module contains handlers for processing chat messages across different interfaces.
"""

import re
from typing import Dict, Any, Optional, List

class ChatMessageHandler:
    """Base class for handling chat messages"""
    
    def __init__(self):
        self.command_patterns = {
            'input': re.compile(r'^input:\s*(.+)', re.IGNORECASE),
            'output': re.compile(r'^output:\s*(.+)', re.IGNORECASE),
            'query': re.compile(r'^query:\s*(.+)', re.IGNORECASE),
            'remember': re.compile(r'^remember:\s*(.+)', re.IGNORECASE),
            'recall': re.compile(r'^recall:\s*(.+)', re.IGNORECASE),
            'help': re.compile(r'^help$', re.IGNORECASE),
            'exit': re.compile(r'^(exit|quit|bye)$', re.IGNORECASE),
        }
    
    def parse_message(self, message: str) -> Dict[str, Any]:
        """Parse a chat message and extract command and content"""
        message = message.strip()
        
        for command, pattern in self.command_patterns.items():
            match = pattern.match(message)
            if match:
                if command in ['input', 'output', 'query', 'remember', 'recall']:
                    return {
                        'type': 'command',
                        'command': command,
                        'content': match.group(1).strip(),
                        'raw_message': message
                    }
                else:
                    return {
                        'type': 'command',
                        'command': command,
                        'content': None,
                        'raw_message': message
                    }
        
        # If no pattern matches, treat as natural language
        return {
            'type': 'natural',
            'content': message,
            'raw_message': message
        }
    
    def format_response(self, response: Any, query: str = None) -> str:
        """Format a response for display"""
        if isinstance(response, str):
            return response
        elif isinstance(response, dict):
            if 'content' in response:
                return response['content']
            elif 'results' in response:
                return response['results']
            else:
                return str(response)
        elif isinstance(response, list) and response:
            return '\n'.join(str(item) for item in response)
        else:
            return "I couldn't process that request."

class CLIMessageHandler(ChatMessageHandler):
    """Handler specifically for CLI interface"""
    
    def format_response(self, response: Any, query: str = None) -> str:
        """Format response for CLI display"""
        formatted = super().format_response(response, query)
        
        # Add CLI-specific formatting
        if query and "No matching memories found" in formatted:
            return f"🤔 {formatted}\nTry saving some memories first with 'input: <your memory>'"
        
        return formatted

class WebMessageHandler(ChatMessageHandler):
    """Handler specifically for web interface"""
    
    def format_response(self, response: Any, query: str = None) -> str:
        """Format response for web display"""
        formatted = super().format_response(response, query)
        
        # Add HTML formatting for web
        formatted = formatted.replace('\n', '<br>')
        formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)
        formatted = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted)
        
        return formatted

class SlackMessageHandler(ChatMessageHandler):
    """Handler for future Slack integration"""
    
    def format_response(self, response: Any, query: str = None) -> str:
        """Format response for Slack display"""
        formatted = super().format_response(response, query)
        
        # Add Slack-specific formatting
        formatted = re.sub(r'\*\*(.*?)\*\*', r'*\1*', formatted)
        
        return formatted

class DiscordMessageHandler(ChatMessageHandler):
    """Handler for future Discord integration"""
    
    def format_response(self, response: Any, query: str = None) -> str:
        """Format response for Discord display"""
        formatted = super().format_response(response, query)
        
        # Add Discord-specific formatting
        formatted = re.sub(r'\*\*(.*?)\*\*', r'**\1**', formatted)
        
        return formatted

# Factory function to get appropriate handler
def get_message_handler(interface_type: str) -> ChatMessageHandler:
    """Get the appropriate message handler for the interface type"""
    handlers = {
        'cli': CLIMessageHandler,
        'web': WebMessageHandler,
        'slack': SlackMessageHandler,
        'discord': DiscordMessageHandler,
    }
    
    handler_class = handlers.get(interface_type, ChatMessageHandler)
    return handler_class()
