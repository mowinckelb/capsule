"""
Chat Configuration
"""

import os

# Chat configuration
CHAT_CONFIG = {
    # CLI settings
    'cli_prompt_format': '{user_id}> ',
    'cli_welcome_message': '🧠 Welcome to Capsule CLI!',
    'cli_goodbye_message': '👋 Goodbye!',
    
    # Command prefixes
    'input_prefixes': ['input:', 'remember:', 'save:'],
    'output_prefixes': ['output:', 'query:', 'recall:', 'ask:'],
    'help_commands': ['help', '?', 'commands'],
    'exit_commands': ['exit', 'quit', 'bye', 'logout'],
    
    # Response formatting
    'success_emoji': '✅',
    'error_emoji': '❌',
    'thinking_emoji': '🤔',
    'memory_emoji': '💾',
    'lightbulb_emoji': '💡',
    'wave_emoji': '👋',
    
    # Message handling
    'max_message_length': int(os.getenv('MAX_MESSAGE_LENGTH', '10000')),
    'enable_natural_language': os.getenv('ENABLE_NATURAL_LANGUAGE', 'true').lower() == 'true',
    'enable_emoji_responses': os.getenv('ENABLE_EMOJI_RESPONSES', 'true').lower() == 'true',
    
    # Interface-specific settings
    'interfaces': {
        'cli': {
            'color_support': os.getenv('CLI_COLOR_SUPPORT', 'true').lower() == 'true',
            'history_size': int(os.getenv('CLI_HISTORY_SIZE', '100')),
        },
        'web': {
            'markdown_support': True,
            'html_formatting': True,
        },
        'slack': {
            'thread_replies': os.getenv('SLACK_THREAD_REPLIES', 'false').lower() == 'true',
            'mention_responses': os.getenv('SLACK_MENTION_RESPONSES', 'true').lower() == 'true',
        },
        'discord': {
            'embed_responses': os.getenv('DISCORD_EMBED_RESPONSES', 'true').lower() == 'true',
            'reaction_confirmations': os.getenv('DISCORD_REACTIONS', 'true').lower() == 'true',
        },
    }
}
