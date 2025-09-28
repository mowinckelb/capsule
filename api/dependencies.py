"""
API Dependencies

This module provides dependency injection for the API routes.
It creates and manages service instances from other modules.
"""

import sys
import os

# Mock imports for when modules aren't available
class MockService:
    def __init__(self, name):
        self.name = name
        print(f"⚠️ Using mock {name} service (module not available)")
    
    def __getattr__(self, name):
        return lambda *args, **kwargs: f"Mock {self.name} response"


def get_database_service():
    """Get database service instance"""
    try:
        # Add database module to path
        database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database')
        if database_path not in sys.path:
            sys.path.append(database_path)
        
        from interface import database_service
        return database_service
    except ImportError:
        return MockService("database")


def get_llm_service():
    """Get LLM service instance"""
    try:
        # Add LLM module to path
        llm_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'llm')
        if llm_path not in sys.path:
            sys.path.append(llm_path)
        
        from interface import llm_service
        return llm_service
    except ImportError:
        return MockService("llm")


def get_auth_service():
    """Get authentication service instance"""
    try:
        # Add authentication module to path
        auth_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'authentication')
        if auth_path not in sys.path:
            sys.path.append(auth_path)
        
        from interface import auth_service
        return auth_service
    except ImportError:
        return MockService("authentication")


def health_check_all_services():
    """Check health of all services"""
    services = {
        'database': get_database_service(),
        'llm': get_llm_service(),
        'authentication': get_auth_service()
    }
    
    health_status = {}
    for name, service in services.items():
        try:
            if hasattr(service, 'health_check'):
                health_status[name] = service.health_check()
            else:
                health_status[name] = False
        except Exception:
            health_status[name] = False
    
    return health_status
