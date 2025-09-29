# Capsule Agents Architecture

## Overview

Capsule is a sophisticated personal memory system that leverages AI agents to create an intelligent, context-aware memory management platform. The system employs multiple specialized agents working together to provide a seamless experience for storing, processing, and retrieving personal memories through natural language interactions.

## Core Agent Types

### 1. LLM Agent (`llm/llm.py`)

The Language Model Agent serves as the central intelligence coordinator for all natural language processing tasks.

#### Capabilities
- **Input Processing**: Refines raw user input into structured, searchable formats
- **Query Optimization**: Transforms natural language questions into effective database queries
- **Response Generation**: Creates natural, contextual responses from retrieved data
- **Multi-modal Support**: Handles text and future image/tool inputs through MCP (Model Context Protocol)

#### Configuration
- **Providers**: Supports Grok, Anthropic Claude, and OpenAI GPT models
- **Default Provider**: Grok (grok-4 model)
- **System Prompt**: Specialized for memory processing and vector database optimization
- **Parameters**: Configurable temperature (0.7), max tokens (4000), and timeout (30s)

#### Processing Flow
```python
# Input processing example
refined_memory = llm_agent.process_input(
    user_id="user123",
    input_text="I had a great lunch at Mario's restaurant",
    is_query=False,
    db_provider="pinecone"
)
# Output: {"summary": "Lunch at Mario's restaurant", "tags": ["lunch", "Mario's", "restaurant", "food", "dining"]}
```

### 2. Database Agent (`database/database.py`)

The Database Agent manages all persistent storage and retrieval operations using vector databases.

#### Capabilities
- **Memory Storage**: Stores processed memories with semantic embeddings
- **Semantic Search**: Performs similarity-based retrieval using vector search
- **User Isolation**: Maintains separate memory spaces for each user
- **Provider Abstraction**: Supports multiple vector database backends

#### Supported Providers
- **Pinecone**: Cloud-native vector database (default)
- **Chroma**: Local persistent vector database
- **Qdrant**: Self-hosted vector database option

#### Vector Processing
- **Embedding Model**: `all-MiniLM-L6-v2` by default
- **Dimensions**: 384-dimensional vectors
- **Distance Metric**: Cosine similarity
- **Batch Processing**: Optimized for performance

### 3. Authentication Agent (`authentication/auth.py`)

The Authentication Agent manages user identity, access control, and session management.

#### Capabilities
- **User Registration**: Secure account creation with password hashing
- **Authentication**: Validates user credentials using Argon2 hashing
- **Session Management**: Maintains user context across interactions
- **Security**: Implements best practices for password storage and validation

#### Security Features
- **Argon2 Password Hashing**: Industry-standard password protection
- **User Isolation**: Ensures data privacy between users
- **Session Validation**: Verifies user identity for all operations

### 4. Chat Interface Agents (`chat/handlers.py`, `chat/cli.py`)

Multiple specialized chat agents handle different interface types and communication patterns.

#### Chat Message Handler Agent
- **Command Parsing**: Recognizes structured commands (input:, output:, query:, remember:, recall:)
- **Natural Language Processing**: Handles conversational inputs
- **Response Formatting**: Tailors output for different interfaces

#### Interface-Specific Agents
- **CLI Agent**: Command-line interface with terminal-optimized formatting
- **Web Agent**: HTML-formatted responses with rich markup
- **Slack Agent**: Slack-compatible message formatting (extensible)
- **Discord Agent**: Discord-compatible message formatting (extensible)

### 5. API Orchestration Agent (`api/server.py`)

The API Agent coordinates between all other agents and manages the overall system workflow.

#### Capabilities
- **Request Routing**: Directs requests to appropriate agents
- **Workflow Orchestration**: Manages multi-step agent interactions
- **Error Handling**: Provides robust error recovery and user feedback
- **Integration Management**: Coordinates between LLM, database, and auth agents

## Agent Interaction Patterns

### Memory Storage Workflow
```
User Input → LLM Agent (processing) → Database Agent (storage) → Confirmation Response
```

1. User provides natural language input
2. LLM Agent processes and structures the input
3. Database Agent stores with semantic embeddings
4. System confirms successful storage

### Memory Retrieval Workflow
```
User Query → LLM Agent (optimization) → Database Agent (search) → LLM Agent (response) → User
```

1. User asks a question in natural language
2. LLM Agent optimizes query for semantic search
3. Database Agent performs vector similarity search
4. LLM Agent generates natural language response
5. Response delivered to user through interface agent

### Authentication Workflow
```
User Credentials → Auth Agent (validation) → Session Creation → Access Grant
```

## Configuration and Extensibility

### Provider Configuration (`config/providers.py`)

The system uses a provider-based architecture for easy extensibility:

```python
# Adding new LLM provider
LLM_PROVIDERS['new_provider'] = {
    'api_key_env': 'NEW_PROVIDER_KEY',
    'base_url': 'https://api.newprovider.com',
    'model': 'model-name',
    'system_prompt': 'Custom prompt...',
    # ... other settings
}
```

### Environment Variables
```bash
# LLM Configuration
DEFAULT_LLM_PROVIDER=grok
GROK_API_KEY=your_grok_key
GROK_MAX_TOKENS=4000
GROK_TEMPERATURE=0.7

# Database Configuration
DEFAULT_DATABASE_PROVIDER=pinecone
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=capsule-data

# Security
ARGON2_TIME_COST=2
ARGON2_MEMORY_COST=65536
```

## Agent Communication Protocols

### Inter-Agent Messaging
Agents communicate through standardized interfaces:

```python
# Agent interface pattern
class AgentInterface:
    def process_input(self, user_id: str, input_data: Any) -> Any
    def health_check(self) -> bool
    def get_provider(self) -> str
```

### Error Handling
Each agent implements robust error handling with graceful degradation:

```python
try:
    result = agent.process_input(user_id, data)
except ProviderError:
    # Fallback to alternative provider
except ValidationError:
    # Return user-friendly error message
except SystemError:
    # Log error and return system unavailable
```

## Deployment and Scaling

### Multi-Interface Support
The agent system supports multiple simultaneous interfaces:
- **Web Interface**: FastAPI-based REST endpoints
- **CLI Interface**: Terminal-based interaction
- **API Interface**: Programmatic access
- **Future Interfaces**: Slack, Discord, mobile apps

### Performance Optimization
- **Async Operations**: Non-blocking agent interactions
- **Connection Pooling**: Efficient resource management
- **Caching**: Embedding and response caching
- **Batch Processing**: Optimized for multiple operations

### Monitoring and Health Checks
Each agent provides health check endpoints for system monitoring:

```python
def health_check(self) -> Dict[str, Any]:
    return {
        'status': 'healthy',
        'provider': self.get_provider(),
        'last_activity': self.last_activity,
        'processed_requests': self.request_count
    }
```

## Security Considerations

### Data Privacy
- **User Isolation**: Each user's memories are completely isolated
- **Encryption**: Sensitive data encrypted at rest and in transit
- **Access Control**: Authentication required for all operations

### API Security
- **Rate Limiting**: Prevents abuse of AI services
- **Input Validation**: Sanitizes all user inputs
- **Audit Logging**: Tracks all system interactions

## Future Extensions

### Planned Agent Enhancements
1. **Multi-Modal Agent**: Support for image, audio, and document processing
2. **Scheduling Agent**: Time-based memory triggers and reminders
3. **Analytics Agent**: Memory pattern analysis and insights
4. **Synchronization Agent**: Cross-device memory synchronization
5. **Export Agent**: Data portability and backup management

### Integration Opportunities
- **Calendar Integration**: Context-aware scheduling
- **Email Integration**: Automatic memory extraction
- **Social Media Integration**: Curated memory collection
- **IoT Integration**: Environmental context awareness

## Usage Examples

### CLI Agent Interaction
```bash
user123> input: Had coffee with Sarah at Blue Bottle this morning, discussed the new project
💾 Memory saved successfully!

user123> output: Where did I meet with Sarah?
💡 You met with Sarah at Blue Bottle coffee shop this morning to discuss the new project.
```

### API Agent Interaction
```python
import requests

# Store memory
response = requests.post("/api/v1/memories", 
    json={"content": "Finished reading Dune - amazing book about politics and ecology"},
    headers={"Authorization": "Bearer user_token"}
)

# Query memories
response = requests.post("/api/v1/query",
    json={"query": "What books have I read recently?"},
    headers={"Authorization": "Bearer user_token"}
)
```

## Conclusion

The Capsule agent architecture provides a robust, extensible foundation for personal memory management. By leveraging specialized agents for different aspects of the system (LLM processing, database operations, authentication, and interface management), the platform offers both powerful functionality and maintainable code organization.

The modular design allows for easy extension with new providers, interfaces, and capabilities while maintaining system reliability and user data security. This agent-based approach ensures that Capsule can evolve and adapt to new technologies and user needs while preserving the core personal memory management experience.