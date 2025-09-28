"""
Frontend Configuration
"""

import os

# Frontend configuration
FRONTEND_CONFIG = {
    # Paths
    'components_dir': 'components',
    'static_dir': 'static',
    'js_dir': 'static/js',
    'css_dir': 'static/css',
    
    # Files
    'landing_page': 'landing.html',
    'interface_page': 'interface.html',
    'main_js': 'app.js',
    'config_js': 'config.js',
    
    # Development settings
    'debug': os.getenv('FRONTEND_DEBUG', 'false').lower() == 'true',
    'hot_reload': os.getenv('FRONTEND_HOT_RELOAD', 'false').lower() == 'true',
    
    # API settings
    'api_base_url': os.getenv('API_BASE_URL', 'http://localhost:8000'),
    'api_timeout': int(os.getenv('API_TIMEOUT', '30')),
    
    # UI settings
    'theme': os.getenv('FRONTEND_THEME', 'light'),
    'enable_dark_mode': os.getenv('ENABLE_DARK_MODE', 'false').lower() == 'true',
    'animation_duration': int(os.getenv('ANIMATION_DURATION', '200')),
    
    # Feature flags
    'enable_keyboard_shortcuts': os.getenv('ENABLE_KEYBOARD_SHORTCUTS', 'true').lower() == 'true',
    'enable_auto_save': os.getenv('ENABLE_AUTO_SAVE', 'false').lower() == 'true',
    'enable_offline_mode': os.getenv('ENABLE_OFFLINE_MODE', 'false').lower() == 'true',
}
