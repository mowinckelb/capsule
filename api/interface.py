"""
API Module Interface - Clean abstraction layer for other modules

This is what other modules import to interact with API functionality.
"""

from routes import api_routes
from server import create_app
from dependencies import health_check_all_services

class APIService:
    """
    API service that provides a clean interface to other modules
    """
    
    def __init__(self):
        self.routes = api_routes
    
    def get_app(self):
        """Get the FastAPI application"""
        return self.routes.get_app()
    
    def create_app(self):
        """Create a new FastAPI application instance"""
        return create_app()
    
    def health_check(self):
        """Check if API service is healthy"""
        try:
            app = self.get_app()
            # Simple check - if we can get the app, API is healthy
            return app is not None
        except Exception:
            return False
    
    def get_service_health(self):
        """Get health status of all integrated services"""
        return health_check_all_services()
    
    def get_routes_info(self):
        """Get information about available routes"""
        app = self.get_app()
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                routes.append({
                    'path': route.path,
                    'methods': list(route.methods) if route.methods else ['GET']
                })
        return routes

# Global service instance that other modules can import
api_service = APIService()
