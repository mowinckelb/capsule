"""
Frontend Module Interface - Clean abstraction layer for other modules

This is what other modules import to interact with frontend functionality.
"""

import os
from pathlib import Path

class FrontendService:
    """
    Frontend service that provides a clean interface to other modules
    """
    
    def __init__(self):
        self.frontend_dir = Path(__file__).parent
        self.components_dir = self.frontend_dir / "components"
        self.static_dir = self.frontend_dir / "static"
        self.static_files = self._discover_static_files()
    
    def _discover_static_files(self):
        """Discover all static frontend files"""
        static_files = {}
        
        # Discover JavaScript files
        js_dir = self.static_dir / "js"
        if js_dir.exists():
            static_files['js'] = [f.name for f in js_dir.glob("*.js")]
        
        # Discover CSS files
        css_dir = self.static_dir / "css"
        if css_dir.exists():
            static_files['css'] = [f.name for f in css_dir.glob("*.css")]
        
        # Discover HTML components
        if self.components_dir.exists():
            static_files['components'] = [f.name for f in self.components_dir.glob("*.html")]
        
        return static_files
    
    def get_landing_page_path(self):
        """Get path to the landing page"""
        return self.components_dir / "landing.html"
    
    def get_interface_page_path(self):
        """Get path to the main interface"""
        return self.components_dir / "interface.html"
    
    def get_static_file_path(self, file_type, filename):
        """Get path to a specific static file"""
        if file_type == 'js':
            return self.static_dir / "js" / filename
        elif file_type == 'css':
            return self.static_dir / "css" / filename
        elif file_type == 'components':
            return self.components_dir / filename
        else:
            raise ValueError(f"Unknown file type: {file_type}")
    
    def list_static_files(self):
        """List all available static files"""
        return self.static_files
    
    def get_app_js_path(self):
        """Get path to the main app JavaScript file"""
        return self.static_dir / "js" / "app.js"
    
    def get_config_js_path(self):
        """Get path to the config JavaScript file"""
        return self.static_dir / "js" / "config.js"
    
    def health_check(self):
        """Check if frontend service is healthy"""
        try:
            # Check if essential files exist
            landing_exists = self.get_landing_page_path().exists()
            interface_exists = self.get_interface_page_path().exists()
            app_js_exists = self.get_app_js_path().exists()
            
            return {
                'healthy': landing_exists and interface_exists and app_js_exists,
                'landing_page': landing_exists,
                'interface_page': interface_exists,
                'app_js': app_js_exists,
                'static_files': self.static_files
            }
        except Exception:
            return {'healthy': False, 'error': 'Health check failed'}

# Global service instance that other modules can import
frontend_service = FrontendService()
