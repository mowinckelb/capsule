"""
Config Integration File

This imports the configuration functionality from the config module.
Other parts of the application import from here.
"""

import sys
import os

# Add the config module to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config'))

from config.interface import config_service
from config.providers import LLM_PROVIDERS, DATABASE_PROVIDERS, DEFAULT_LLM_PROVIDER, DEFAULT_DATABASE_PROVIDER
from config.settings import APP_CONFIG, SERVER_CONFIG, FEATURE_FLAGS
from config.environment import env, is_development, is_production

# Export for backward compatibility with existing code (maintain old names)
__all__ = [
    'config_service', 
    'LLM_PROVIDERS', 'DATABASE_PROVIDERS', 
    'DEFAULT_LLM_PROVIDER', 'DEFAULT_DATABASE_PROVIDER',
    'APP_CONFIG', 'SERVER_CONFIG', 'FEATURE_FLAGS',
    'env', 'is_development', 'is_production',
    # Old names for compatibility
    'PROVIDERS', 'DB_PROVIDERS', 'DEFAULT_PROVIDER', 'DEFAULT_DB_PROVIDER'
]

# Backward compatibility aliases
PROVIDERS = LLM_PROVIDERS
DB_PROVIDERS = DATABASE_PROVIDERS
DEFAULT_PROVIDER = DEFAULT_LLM_PROVIDER
DEFAULT_DB_PROVIDER = DEFAULT_DATABASE_PROVIDER

print("✅ Config integration loaded")
