import sqlite3
import os
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import AUTH_CONFIG

class AuthHandler:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
        self.db_path = AUTH_CONFIG['db_path']
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database for users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, hashed_password TEXT)")
        conn.commit()
        conn.close()
        print("✅ Authentication database initialized")
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        # Truncate password to 72 bytes for argon2 compatibility
        truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return self.pwd_context.hash(truncated_password)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return self.pwd_context.verify(truncated_password, hashed_password)
    
    def register_user(self, user_id: str, password: str) -> bool:
        """Register a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if user already exists
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            if cursor.fetchone():
                conn.close()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID exists")
            
            # Hash password and insert user
            hashed_password = self.hash_password(password)
            cursor.execute("INSERT INTO users (user_id, hashed_password) VALUES (?, ?)", (user_id, hashed_password))
            conn.commit()
            conn.close()
            return True
            
        except HTTPException:
            conn.close()
            raise
        except Exception as e:
            conn.close()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Registration failed: {str(e)}")
    
    def authenticate_user(self, user_id: str, password: str) -> bool:
        """Authenticate a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT hashed_password FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            conn.close()
            
            if not user or not self.verify_password(password, user[0]):
                return False
            return True
            
        except Exception:
            conn.close()
            return False
    
    def login_user(self, form_data: OAuth2PasswordRequestForm) -> dict:
        """Login a user and return access token"""
        if not self.authenticate_user(form_data.username, form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Wrong password or user ID"
            )
        
        # In this simple implementation, we use the username as the token
        # In production, you'd want to use JWT or similar
        return {
            "access_token": form_data.username, 
            "token_type": "bearer"
        }
    
    def get_current_user(self, token: str) -> dict:
        """Get current user from token"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (token,))
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid credentials"
                )
            
            return {"user_id": user[0]}
            
        except HTTPException:
            raise
        except Exception:
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials"
            )
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return deleted
            
        except Exception:
            conn.close()
            return False
    
    def list_users(self) -> list:
        """List all users (for admin purposes)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT user_id FROM users")
            users = [row[0] for row in cursor.fetchall()]
            conn.close()
            return users
            
        except Exception:
            conn.close()
            return []
    
    def health_check(self) -> bool:
        """Check if authentication system is healthy"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            cursor.fetchone()
            conn.close()
            return True
        except Exception:
            return False

if __name__ == "__main__":
    # Test the authentication system
    auth = AuthHandler()
    print("Authentication system test:")
    print(f"Health check: {auth.health_check()}")
    print(f"Users: {auth.list_users()}")
