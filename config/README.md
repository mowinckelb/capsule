# Config Module

This is a **self-contained configuration module** that manages all application settings and provider configurations.

## 📁 Structure

```
config/
├── settings.py         # Application, server, and feature settings
├── providers.py        # LLM and database provider configurations
├── environment.py      # Environment variable management
├── interface.py        # Clean interface for other modules
├── test_config.py     # Comprehensive tests (future)
├── __init__.py        # Module initialization
└── README.md         # This file
```

## 🔧 Usage

### For Other Modules:
```python
from config import config_service

# Get configurations
app_config = config_service.get_app_config()
llm_config = config_service.get_llm_provider_config('grok')
db_config = config_service.get_database_provider_config('pinecone')

# Check features
if config_service.is_feature_enabled('enable_metrics'):
    # Enable metrics collection

# Environment checks
if config_service.is_development():
    # Development-specific code
```

### For Direct Access:
```python
# Import specific configurations
from config.settings import APP_CONFIG, FEATURE_FLAGS
from config.providers import LLM_PROVIDERS, DEFAULT_LLM_PROVIDER
from config.environment import env, is_development

# Access environment variables with validation
api_key = env.require('GROK_API_KEY', 'Required for LLM functionality')
debug_mode = env.get('DEBUG', False, bool, 'Enable debug mode')
```

### For Environment Management:
```python
from config.environment import EnvironmentManager

# Create custom environment manager
env_manager = EnvironmentManager('.env.production')

# Validate all required variables
env_manager.validate_all()

# Get environment summary
summary = env_manager.get_summary()
```

## ⚙️ Configuration Categories

### Application Settings (`settings.py`)
- **App Config**: Name, version, environment, debug settings
- **Server Config**: Host, port, CORS, worker settings
- **Database Config**: SQLite paths, backup settings
- **Security Config**: Password hashing, JWT settings
- **Feature Flags**: Toggle features on/off
- **Rate Limiting**: API rate limiting configuration
- **Logging**: Log file settings and formats

### Provider Settings (`providers.py`)
- **LLM Providers**: Grok, Anthropic, OpenAI configurations
- **Database Providers**: Pinecone, Chroma, Qdrant configurations
- **Embedding Config**: Model settings and caching
- **Default Providers**: Which providers to use by default

### Environment Management (`environment.py`)
- **Variable Loading**: Automatic .env file loading
- **Type Conversion**: String to bool/int/float/list conversion
- **Validation**: Required vs optional variable checking
- **Summary**: Overview of all environment settings

## 🌍 Environment Variables

### Required Variables:
```bash
# LLM Provider (choose one)
GROK_API_KEY=your-grok-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
OPENAI_API_KEY=your-openai-api-key

# Database Provider (choose one)
PINECONE_API_KEY=your-pinecone-api-key
```

### Optional Variables:
```bash
# Application
ENVIRONMENT=development          # development, production, testing
DEBUG=false                     # Enable debug mode
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR

# Server
HOST=0.0.0.0                   # Server host
PORT=8000                      # Server port
CORS_ORIGINS=*                 # Comma-separated origins

# Providers
DEFAULT_LLM_PROVIDER=grok      # Default LLM provider
DEFAULT_DATABASE_PROVIDER=pinecone  # Default database provider

# Features
ENABLE_REGISTRATION=true       # Allow new user registration
ENABLE_METRICS=false          # Collect usage metrics
ENABLE_RATE_LIMITING=true     # Enable API rate limiting

# Security
SECRET_KEY=your-secret-key     # JWT secret key
TOKEN_EXPIRE_MINUTES=1440      # Token expiration (24 hours)
```

## 🎯 Provider Configurations

### LLM Providers:
- **Grok**: X.AI's Grok model
- **Anthropic**: Claude models
- **OpenAI**: GPT models

### Database Providers:
- **Pinecone**: Managed vector database
- **Chroma**: Local vector database
- **Qdrant**: Self-hosted vector database

### Adding New Providers:
```python
# In providers.py
LLM_PROVIDERS['new_provider'] = {
    'api_key_env': 'NEW_PROVIDER_API_KEY',
    'base_url': 'https://api.newprovider.com',
    'model': 'new-model-v1',
    'system_prompt': 'Custom prompt...',
}
```

## 🧪 Features & Flags

Current feature flags:
- `enable_registration` - Allow new user registration
- `enable_guest_mode` - Allow guest access
- `enable_metrics` - Collect usage metrics
- `enable_rate_limiting` - API rate limiting
- `enable_caching` - Response caching

## 🔄 Development Workflow

1. **Work on this branch**: `feature/config`
2. **Make improvements**: Modify any files in this folder
3. **Test settings**: Validate with different environments
4. **Test providers**: Ensure provider configs work
5. **Commit changes**: All config changes in one commit
6. **Merge to develop**: Only when thoroughly tested

## 🚀 Advanced Features

### Environment Validation:
```python
from config import config_service

# Validate all configuration
validation = config_service.validate_configuration()
if not validation['valid']:
    print("Configuration issues:", validation['issues'])
```

### Health Checks:
```python
health = config_service.health_check()
print(f"Config healthy: {health['healthy']}")
```

### Dynamic Configuration:
```python
# Check if features are enabled
if config_service.is_feature_enabled('enable_metrics'):
    start_metrics_collection()

# Get provider-specific settings
if config_service.get_default_llm_provider() == 'grok':
    setup_grok_client()
```

## 🎯 Independence

This module is **completely isolated**:
- ✅ No dependencies on other feature branches
- ✅ Self-contained configuration management
- ✅ Environment variable validation
- ✅ Provider abstraction layer
- ✅ Clean interface for all modules

You can improve this module without affecting any other features!
