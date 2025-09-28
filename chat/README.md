# Chat Module

This is a **self-contained chat module** that provides command-line and future chat interfaces.

## 📁 Structure

```
chat/
├── cli.py              # Command-line interface implementation
├── handlers.py         # Message handlers for different interfaces
├── interface.py        # Clean interface for other modules
├── config.py          # Chat configuration
├── test_chat.py       # Comprehensive tests (future)
├── __init__.py        # Module initialization
└── README.md         # This file
```

## 🔧 Usage

### For Other Modules:
```python
from chat import chat_service

# Run CLI interface
chat_service.run_cli()

# Parse messages
parsed = chat_service.parse_message("input: test memory", "cli")

# Format responses
formatted = chat_service.format_response(response, query, "web")

# Get specific handler
handler = chat_service.get_message_handler("slack")
```

### Direct CLI Usage:
```bash
# Run from chat directory
cd chat/
python cli.py

# Or run as module
python -m chat.cli
```

### For Development:
```bash
# Test the CLI
python cli.py

# Test individual components
python handlers.py     # Test message handlers
python interface.py    # Test interface
```

## 💬 Interfaces

### CLI Interface (`cli.py`)
- **Interactive Command Line**: Full authentication and chat loop
- **Commands**: `input:`, `output:`, `help`, `exit`
- **Authentication**: Login/register flow
- **Error Handling**: User-friendly error messages
- **Session Management**: Maintains user context

### Message Handlers (`handlers.py`)
- **CLI Handler**: Terminal-optimized responses
- **Web Handler**: HTML formatting for web interface
- **Slack Handler**: Slack-specific formatting (future)
- **Discord Handler**: Discord-specific formatting (future)

## 🎯 Commands

### Memory Commands:
- `input: <memory>` - Save a new memory
- `remember: <memory>` - Alternative save command
- `save: <memory>` - Another save alternative

### Query Commands:
- `output: <question>` - Ask a question
- `query: <question>` - Alternative query command
- `recall: <question>` - Alternative recall command
- `ask: <question>` - Another query alternative

### System Commands:
- `help` - Show available commands
- `exit` - Quit the session
- `quit` - Alternative exit command

## 🧪 Features

- ✅ **Multi-Interface Support**: CLI, Web, Slack, Discord ready
- ✅ **Command Parsing**: Flexible command recognition
- ✅ **Natural Language**: Support for natural language processing
- ✅ **Authentication**: Integrated user management
- ✅ **Error Handling**: Graceful error recovery
- ✅ **Configurable**: Extensive configuration options
- ✅ **Extensible**: Easy to add new interfaces

## 🔄 Development Workflow

1. **Work on this branch**: `feature/chat`
2. **Make improvements**: Modify any files in this folder
3. **Test CLI**: `python cli.py`
4. **Test handlers**: Run individual handler tests
5. **Commit changes**: All chat changes in one commit
6. **Merge to develop**: Only when thoroughly tested

## 🚀 Future Enhancements

### Slack Integration:
```python
# Future slack bot
from chat.handlers import SlackMessageHandler
handler = SlackMessageHandler()
```

### Discord Integration:
```python
# Future discord bot
from chat.handlers import DiscordMessageHandler
handler = DiscordMessageHandler()
```

### Advanced Features:
- **Voice Interface**: Speech-to-text integration
- **Multi-user Chat**: Group conversations
- **Rich Media**: Image and file support
- **Context Awareness**: Conversation history
- **Templates**: Pre-defined response templates

## 🎯 Independence

This module is **completely isolated**:
- ✅ No dependencies on other feature branches
- ✅ Self-contained CLI application
- ✅ Independent testing and development
- ✅ Clean interface for integration
- ✅ Configurable for different environments

You can improve this module without affecting any other features!
