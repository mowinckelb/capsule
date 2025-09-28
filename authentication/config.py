# Authentication configuration for the authentication module
# This is self-contained within the authentication feature branch

import os

# Authentication configuration
AUTH_CONFIG = {
    'db_path': 'users.db',
    'password_schemes': ['argon2'],
    'token_url': 'login',
    'max_password_length': 72,  # For argon2 compatibility
    'session_expire_hours': 24
}

# Security settings
SECURITY_CONFIG = {
    'allow_user_registration': True,
    'require_strong_passwords': False,  # Can be enhanced later
    'max_login_attempts': 5,
    'lockout_duration_minutes': 15
}
