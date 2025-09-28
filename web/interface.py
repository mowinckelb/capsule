"""
Web Module Interface - Clean abstraction layer for other modules

This is what other modules import to interact with web functionality.
"""

import os
from pathlib import Path

class WebService:
    """
    Web service that provides a clean interface to other modules
    """
    
    def __init__(self):
        self.web_dir = Path(__file__).parent
        self.static_files = self._discover_static_files()
    
    def _discover_static_files(self):
        """Discover all static web files"""
        static_files = {}
        
        # HTML files
        html_files = list(self.web_dir.glob("*.html"))
        for html_file in html_files:
            static_files[html_file.stem] = str(html_file)
        
        # JavaScript files
        js_files = list(self.web_dir.glob("*.js"))
        for js_file in js_files:
            static_files[js_file.stem] = str(js_file)
        
        # CSS files (if any)
        css_files = list(self.web_dir.glob("*.css"))
        for css_file in css_files:
            static_files[css_file.stem] = str(css_file)
        
        return static_files
    
    def get_static_files(self):
        """Get all static files for serving"""
        return self.static_files
    
    def get_main_interface(self):
        """Get the main HTML interface file"""
        interface_path = self.web_dir / "interface.html"
        if interface_path.exists():
            return str(interface_path)
        return None
    
    def get_app_js(self):
        """Get the main JavaScript application file"""
        app_js_path = self.web_dir / "app.js"
        if app_js_path.exists():
            return str(app_js_path)
        return None
    
    def get_config_js(self):
        """Get the JavaScript configuration file"""
        config_js_path = self.web_dir / "config.js"
        if config_js_path.exists():
            return str(config_js_path)
        return None
    
    def read_file(self, filename):
        """Read a web file's contents"""
        file_path = self.web_dir / filename
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        return None
    
    def health_check(self):
        """Check if web interface files are available"""
        try:
            # Check if main files exist
            main_interface = self.get_main_interface()
            app_js = self.get_app_js()
            
            return main_interface is not None and app_js is not None
        except Exception:
            return False
    
    def get_file_info(self):
        """Get information about web files"""
        info = {
            'total_files': len(self.static_files),
            'files': list(self.static_files.keys()),
            'main_interface': self.get_main_interface() is not None,
            'app_js': self.get_app_js() is not None,
            'config_js': self.get_config_js() is not None
        }
        return info
    
    def serve_directory(self):
        """Get the directory to serve static files from"""
        return str(self.web_dir)

# Global service instance that other modules can import
web_service = WebService()
