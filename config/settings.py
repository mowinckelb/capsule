"""
Capsule Configuration Settings

Centralized configuration for all modules with environment variable support.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application settings
APP_CONFIG = {
    'name': 'Capsule',
    'version': '1.0.0',
    'description': 'Personal Memory System',
    'environment': os.getenv('ENVIRONMENT', 'development'),
    'debug': os.getenv('DEBUG', 'false').lower() == 'true',
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
}

# Server settings
SERVER_CONFIG = {
    'host': os.getenv('HOST', '0.0.0.0'),
    'port': int(os.getenv('PORT', '8000')),
    'reload': os.getenv('RELOAD', 'false').lower() == 'true',
    'workers': int(os.getenv('WORKERS', '1')),
    'cors_origins': os.getenv('CORS_ORIGINS', '*').split(','),
}

# Database settings
DATABASE_CONFIG = {
    'users_db_path': os.getenv('USERS_DB_PATH', 'users.db'),
    'backup_interval': int(os.getenv('BACKUP_INTERVAL', '3600')),  # seconds
    'max_connections': int(os.getenv('MAX_DB_CONNECTIONS', '10')),
}

# Security settings
SECURITY_CONFIG = {
    'password_schemes': ['argon2'],
    'password_deprecated': 'auto',
    'token_expire_minutes': int(os.getenv('TOKEN_EXPIRE_MINUTES', '1440')),  # 24 hours
    'secret_key': os.getenv('SECRET_KEY', 'your-secret-key-change-this'),
    'algorithm': 'HS256',
}

# Feature flags
FEATURE_FLAGS = {
    'enable_registration': os.getenv('ENABLE_REGISTRATION', 'true').lower() == 'true',
    'enable_guest_mode': os.getenv('ENABLE_GUEST_MODE', 'false').lower() == 'true',
    'enable_metrics': os.getenv('ENABLE_METRICS', 'false').lower() == 'true',
    'enable_rate_limiting': os.getenv('ENABLE_RATE_LIMITING', 'true').lower() == 'true',
    'enable_caching': os.getenv('ENABLE_CACHING', 'true').lower() == 'true',
}

# Rate limiting settings
RATE_LIMIT_CONFIG = {
    'requests_per_minute': int(os.getenv('REQUESTS_PER_MINUTE', '60')),
    'burst_limit': int(os.getenv('BURST_LIMIT', '10')),
    'enable_per_user_limits': os.getenv('PER_USER_LIMITS', 'true').lower() == 'true',
}

# Logging settings
LOGGING_CONFIG = {
    'log_file': os.getenv('LOG_FILE', 'capsule.log'),
    'max_log_size': int(os.getenv('MAX_LOG_SIZE', '10485760')),  # 10MB
    'backup_count': int(os.getenv('LOG_BACKUP_COUNT', '5')),
    'log_format': os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
}
