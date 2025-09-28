"""
Config Module Interface - Clean abstraction layer for other modules

This is what other modules import to interact with configuration.
"""

from .settings import (
    APP_CONFIG, SERVER_CONFIG, DATABASE_CONFIG, SECURITY_CONFIG,
    FEATURE_FLAGS, RATE_LIMIT_CONFIG, LOGGING_CONFIG
)
from .providers import (
    LLM_PROVIDERS, DATABASE_PROVIDERS, DEFAULT_LLM_PROVIDER,
    DEFAULT_DATABASE_PROVIDER, EMBEDDING_CONFIG
)
from .environment import env, is_development, is_production, is_testing

class ConfigService:
    """
    Configuration service that provides a clean interface to other modules
    """
    
    def __init__(self):
        self._cached_config = None
    
    def get_app_config(self):
        """Get application configuration"""
        return APP_CONFIG.copy()
    
    def get_server_config(self):
        """Get server configuration"""
        return SERVER_CONFIG.copy()
    
    def get_database_config(self):
        """Get database configuration"""
        return DATABASE_CONFIG.copy()
    
    def get_security_config(self):
        """Get security configuration"""
        return SECURITY_CONFIG.copy()
    
    def get_feature_flags(self):
        """Get feature flags"""
        return FEATURE_FLAGS.copy()
    
    def get_llm_providers(self):
        """Get LLM provider configurations"""
        return LLM_PROVIDERS.copy()
    
    def get_database_providers(self):
        """Get database provider configurations"""
        return DATABASE_PROVIDERS.copy()
    
    def get_default_llm_provider(self):
        """Get default LLM provider name"""
        return DEFAULT_LLM_PROVIDER
    
    def get_default_database_provider(self):
        """Get default database provider name"""
        return DEFAULT_DATABASE_PROVIDER
    
    def get_llm_provider_config(self, provider_name: str = None):
        """Get configuration for a specific LLM provider"""
        provider = provider_name or DEFAULT_LLM_PROVIDER
        if provider not in LLM_PROVIDERS:
            raise ValueError(f"Unknown LLM provider: {provider}")
        return LLM_PROVIDERS[provider].copy()
    
    def get_database_provider_config(self, provider_name: str = None):
        """Get configuration for a specific database provider"""
        provider = provider_name or DEFAULT_DATABASE_PROVIDER
        if provider not in DATABASE_PROVIDERS:
            raise ValueError(f"Unknown database provider: {provider}")
        return DATABASE_PROVIDERS[provider].copy()
    
    def get_embedding_config(self):
        """Get embedding configuration"""
        return EMBEDDING_CONFIG.copy()
    
    def is_feature_enabled(self, feature_name: str):
        """Check if a feature is enabled"""
        return FEATURE_FLAGS.get(feature_name, False)
    
    def get_environment(self):
        """Get current environment"""
        return APP_CONFIG['environment']
    
    def is_development(self):
        """Check if running in development mode"""
        return is_development()
    
    def is_production(self):
        """Check if running in production mode"""
        return is_production()
    
    def is_testing(self):
        """Check if running in test mode"""
        return is_testing()
    
    def get_all_config(self):
        """Get all configuration as a single dictionary"""
        if not self._cached_config:
            self._cached_config = {
                'app': self.get_app_config(),
                'server': self.get_server_config(),
                'database': self.get_database_config(),
                'security': self.get_security_config(),
                'features': self.get_feature_flags(),
                'llm_providers': self.get_llm_providers(),
                'database_providers': self.get_database_providers(),
                'embedding': self.get_embedding_config(),
                'environment': {
                    'current': self.get_environment(),
                    'is_development': self.is_development(),
                    'is_production': self.is_production(),
                    'is_testing': self.is_testing()
                }
            }
        return self._cached_config.copy()
    
    def validate_configuration(self):
        """Validate all configuration settings"""
        issues = []
        
        # Check required API keys for enabled providers
        llm_provider = self.get_default_llm_provider()
        llm_config = self.get_llm_provider_config(llm_provider)
        if 'api_key_env' in llm_config:
            api_key = env.get(llm_config['api_key_env'])
            if not api_key:
                issues.append(f"Missing API key for LLM provider '{llm_provider}': {llm_config['api_key_env']}")
        
        db_provider = self.get_default_database_provider()
        db_config = self.get_database_provider_config(db_provider)
        if 'api_key_env' in db_config:
            api_key = env.get(db_config['api_key_env'])
            if not api_key:
                issues.append(f"Missing API key for database provider '{db_provider}': {db_config['api_key_env']}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def health_check(self):
        """Check if configuration service is healthy"""
        try:
            validation = self.validate_configuration()
            config = self.get_all_config()
            
            return {
                'healthy': validation['valid'],
                'validation': validation,
                'default_providers': {
                    'llm': self.get_default_llm_provider(),
                    'database': self.get_default_database_provider()
                },
                'environment': self.get_environment(),
                'feature_count': len(self.get_feature_flags()),
                'provider_count': {
                    'llm': len(self.get_llm_providers()),
                    'database': len(self.get_database_providers())
                }
            }
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }

# Global service instance that other modules can import
config_service = ConfigService()

# For backward compatibility, export the old names
PROVIDERS = LLM_PROVIDERS
DB_PROVIDERS = DATABASE_PROVIDERS
DEFAULT_PROVIDER = DEFAULT_LLM_PROVIDER
DEFAULT_DB_PROVIDER = DEFAULT_DATABASE_PROVIDER
