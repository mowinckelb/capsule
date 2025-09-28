"""
Authentication Module Interface - Clean abstraction layer for other modules

This is what other modules import to interact with authentication functionality.
"""

from auth import AuthHandler

class AuthService:
    """
    Authentication service that provides a clean interface to other modules
    """
    def __init__(self):
        self.auth_handler = AuthHandler()
    
    def register(self, user_id: str, password: str) -> bool:
        """Register a new user"""
        return self.auth_handler.register_user(user_id, password)
    
    def login(self, user_id: str, password: str) -> dict:
        """Login a user and return token info"""
        from fastapi.security import OAuth2PasswordRequestForm
        
        # Create form data object
        class MockFormData:
            def __init__(self, username, password):
                self.username = username
                self.password = password
        
        form_data = MockFormData(user_id, password)
        return self.auth_handler.login_user(form_data)
    
    def authenticate(self, user_id: str, password: str) -> bool:
        """Authenticate a user"""
        return self.auth_handler.authenticate_user(user_id, password)
    
    def get_user_from_token(self, token: str) -> dict:
        """Get user info from token"""
        return self.auth_handler.get_current_user(token)
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        return self.auth_handler.delete_user(user_id)
    
    def list_users(self) -> list:
        """List all users"""
        return self.auth_handler.list_users()
    
    def health_check(self) -> bool:
        """Check if authentication service is healthy"""
        return self.auth_handler.health_check()
    
    def get_oauth2_scheme(self):
        """Get OAuth2 scheme for FastAPI dependency injection"""
        return self.auth_handler.oauth2_scheme
    
    def get_current_user_dependency(self):
        """Get the current user dependency function for FastAPI"""
        return self.auth_handler.get_current_user

# Global service instance that other modules can import
auth_service = AuthService()
