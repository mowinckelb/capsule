# API configuration for the API module
# This is self-contained within the API feature branch

import os

# API application configuration
API_CONFIG = {
    'title': 'Capsule API',
    'description': 'Personal memory storage and retrieval system',
    'version': '1.0.0',
    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 8001)),
    'reload': False,
    'serve_static': True,  # Whether to serve static files
    'debug': os.getenv('DEBUG', 'false').lower() == 'true'
}

# CORS configuration
CORS_CONFIG = {
    'allow_origins': ['*'],
    'allow_credentials': True,
    'allow_methods': ['*'],
    'allow_headers': ['*']
}

# Rate limiting configuration (for future enhancement)
RATE_LIMIT_CONFIG = {
    'requests_per_minute': 60,
    'burst_limit': 10,
    'enabled': False  # Can be enabled later
}
