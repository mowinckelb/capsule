# API Module

## Executive Summary
**What**: FastAPI REST endpoints for authentication, memory storage, and querying. **Why**: Unified API layer for all client interactions. **Agent Instructions**: Use dependency injection, mock unavailable services gracefully, test all endpoints before PRs.

This is a **self-contained API module** that can be developed and tested independently.

## 📁 Structure

```
api/
├── routes.py           # FastAPI routes and endpoints
├── server.py           # Server startup and configuration
├── dependencies.py     # Dependency injection for other modules
├── config.py           # API configuration
├── interface.py        # Clean interface for other modules
├── test_api.py         # Comprehensive tests
├── __init__.py         # Module initialization
└── README.md          # This file
```

## 🔧 Usage

### For Other Modules:
```python
from api import api_service

# Get FastAPI app
app = api_service.get_app()

# Check API health
is_healthy = api_service.health_check()

# Get routes information
routes = api_service.get_routes_info()
```

### For Standalone Server:
```bash
# Run the API server independently
cd api/
python server.py
```

### For Development:
```bash
# Run tests
python test_api.py

# Test individual components
python routes.py        # Test routes
python dependencies.py  # Test dependencies
```

## 🛠️ API Endpoints

### Authentication:
- `POST /register` - Register a new user
- `POST /login` - Login and get access token

### Memory Management:
- `POST /add` - Add a memory (authenticated)
- `GET /query?q=<question>` - Query memories (authenticated)
- `POST /upload` - Upload MCP data (authenticated)

### Admin:
- `GET /health` - Health check of all services
- `GET /users` - List all users (authenticated)

### Static Files:
- `GET /` - Serve static web interface

## 🧪 Testing

Run comprehensive tests:
```bash
cd api/
python test_api.py
```

This tests:
- ✅ Configuration loading
- ✅ FastAPI app creation
- ✅ All API endpoints (with mocks)
- ✅ Dependency injection
- ✅ Interface functionality
- ✅ Health checks

## 🔄 Development Workflow

1. **Work on this branch**: `feature/api`
2. **Make improvements**: Modify any files in this folder
3. **Test thoroughly**: `python test_api.py`
4. **Test server**: `python server.py` 
5. **Commit changes**: All API changes in one commit
6. **Merge to develop**: Only when all tests pass

## 🔌 Dependency Injection

This module uses **smart dependency injection**:
- ✅ **Auto-discovery**: Finds other modules automatically
- ✅ **Graceful degradation**: Uses mocks when modules unavailable
- ✅ **Clean interfaces**: Only imports through module interfaces
- ✅ **Hot-swappable**: Easy to replace implementations

## 🎯 Independence

This module is **completely isolated**:
- ✅ No dependencies on other feature branches
- ✅ Self-contained configuration
- ✅ Independent testing with mocks
- ✅ Can run standalone server
- ✅ Clean interface for other modules

You can improve this module without affecting any other features!
