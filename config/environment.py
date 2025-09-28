"""
Environment Variable Management

Utilities for loading and validating environment variables.
"""

import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

class EnvironmentManager:
    """Manages environment variables with validation and defaults"""
    
    def __init__(self, env_file: str = None):
        """Initialize environment manager"""
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        self.required_vars = set()
        self.optional_vars = {}
    
    def require(self, var_name: str, description: str = ""):
        """Mark an environment variable as required"""
        self.required_vars.add((var_name, description))
        
        if not os.getenv(var_name):
            raise ValueError(f"Required environment variable '{var_name}' is not set. {description}")
        
        return os.getenv(var_name)
    
    def get(self, var_name: str, default: Any = None, var_type: type = str, description: str = ""):
        """Get environment variable with type conversion and default"""
        self.optional_vars[var_name] = {
            'default': default,
            'type': var_type,
            'description': description
        }
        
        value = os.getenv(var_name)
        
        if value is None:
            return default
        
        # Type conversion
        try:
            if var_type == bool:
                return value.lower() in ('true', '1', 'yes', 'on')
            elif var_type == int:
                return int(value)
            elif var_type == float:
                return float(value)
            elif var_type == list:
                return [item.strip() for item in value.split(',') if item.strip()]
            else:
                return var_type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Environment variable '{var_name}' has invalid value '{value}' for type {var_type.__name__}: {e}")
    
    def validate_all(self):
        """Validate all required environment variables are set"""
        missing = []
        for var_name, description in self.required_vars:
            if not os.getenv(var_name):
                missing.append(f"  - {var_name}: {description}")
        
        if missing:
            raise ValueError(f"Missing required environment variables:\n" + "\n".join(missing))
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all environment variables"""
        summary = {
            'required': {},
            'optional': {},
            'missing_required': [],
            'unused_env_vars': []
        }
        
        # Check required vars
        for var_name, description in self.required_vars:
            value = os.getenv(var_name)
            summary['required'][var_name] = {
                'value': '***SET***' if value else None,
                'description': description,
                'is_set': bool(value)
            }
            if not value:
                summary['missing_required'].append(var_name)
        
        # Check optional vars
        for var_name, config in self.optional_vars.items():
            value = os.getenv(var_name)
            summary['optional'][var_name] = {
                'value': value or config['default'],
                'default': config['default'],
                'type': config['type'].__name__,
                'description': config['description'],
                'is_set': bool(value)
            }
        
        # Find unused environment variables (those starting with common prefixes)
        all_known = set(var[0] for var in self.required_vars) | set(self.optional_vars.keys())
        common_prefixes = ['CAPSULE_', 'GROK_', 'PINECONE_', 'ANTHROPIC_', 'OPENAI_']
        
        for env_var in os.environ:
            if any(env_var.startswith(prefix) for prefix in common_prefixes):
                if env_var not in all_known:
                    summary['unused_env_vars'].append(env_var)
        
        return summary

# Global environment manager instance
env = EnvironmentManager()

# Common environment variable patterns
def get_api_key(provider: str, required: bool = True) -> Optional[str]:
    """Get API key for a provider"""
    var_name = f"{provider.upper()}_API_KEY"
    if required:
        return env.require(var_name, f"API key for {provider}")
    else:
        return env.get(var_name, description=f"API key for {provider}")

def get_database_url(provider: str) -> Optional[str]:
    """Get database URL for a provider"""
    var_name = f"{provider.upper()}_URL"
    return env.get(var_name, description=f"Database URL for {provider}")

def is_development() -> bool:
    """Check if running in development mode"""
    return env.get('ENVIRONMENT', 'development').lower() in ('development', 'dev', 'local')

def is_production() -> bool:
    """Check if running in production mode"""
    return env.get('ENVIRONMENT', 'development').lower() in ('production', 'prod')

def is_testing() -> bool:
    """Check if running in test mode"""
    return env.get('ENVIRONMENT', 'development').lower() in ('testing', 'test')

# Load common environment variables
COMMON_ENV_VARS = {
    'DEBUG': env.get('DEBUG', False, bool, "Enable debug mode"),
    'LOG_LEVEL': env.get('LOG_LEVEL', 'INFO', str, "Logging level"),
    'ENVIRONMENT': env.get('ENVIRONMENT', 'development', str, "Application environment"),
    'HOST': env.get('HOST', '0.0.0.0', str, "Server host"),
    'PORT': env.get('PORT', 8000, int, "Server port"),
}
