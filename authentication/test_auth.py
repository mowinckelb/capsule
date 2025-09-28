"""
Authentication Module Tests - Test everything in this module

Run this to test all authentication functionality before merging to develop.
"""

import os
import sys
import unittest
import tempfile
from unittest.mock import Mock, patch

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth import AuthHandler
from interface import auth_service
from config import AUTH_CONFIG, SECURITY_CONFIG


class TestAuthModule(unittest.TestCase):
    """Test the complete authentication module"""
    
    def setUp(self):
        """Set up test fixtures with temporary database"""
        # Use temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Update config to use temp database
        AUTH_CONFIG['db_path'] = self.temp_db.name
        
        # Create fresh auth handler for each test
        self.auth_handler = AuthHandler()
    
    def tearDown(self):
        """Clean up temporary database"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_config_loading(self):
        """Test that configuration loads correctly"""
        self.assertIn('db_path', AUTH_CONFIG)
        self.assertIn('password_schemes', AUTH_CONFIG)
        self.assertIn('allow_user_registration', SECURITY_CONFIG)
    
    def test_auth_service_interface(self):
        """Test the authentication service interface"""
        self.assertIsNotNone(auth_service)
        self.assertTrue(hasattr(auth_service, 'register'))
        self.assertTrue(hasattr(auth_service, 'login'))
        self.assertTrue(hasattr(auth_service, 'authenticate'))
        self.assertTrue(hasattr(auth_service, 'health_check'))
    
    def test_database_initialization(self):
        """Test that database initializes correctly"""
        self.assertTrue(self.auth_handler.health_check())
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "test_password_123"
        hashed = self.auth_handler.hash_password(password)
        
        self.assertNotEqual(password, hashed)
        self.assertTrue(self.auth_handler.verify_password(password, hashed))
        self.assertFalse(self.auth_handler.verify_password("wrong_password", hashed))
    
    def test_user_registration(self):
        """Test user registration"""
        user_id = "test_user"
        password = "test_password"
        
        # Register user
        result = self.auth_handler.register_user(user_id, password)
        self.assertTrue(result)
        
        # Check user exists
        users = self.auth_handler.list_users()
        self.assertIn(user_id, users)
        
        # Try to register same user again (should fail)
        with self.assertRaises(Exception):
            self.auth_handler.register_user(user_id, password)
    
    def test_user_authentication(self):
        """Test user authentication"""
        user_id = "test_user"
        password = "test_password"
        
        # Register user first
        self.auth_handler.register_user(user_id, password)
        
        # Test correct authentication
        self.assertTrue(self.auth_handler.authenticate_user(user_id, password))
        
        # Test wrong password
        self.assertFalse(self.auth_handler.authenticate_user(user_id, "wrong_password"))
        
        # Test non-existent user
        self.assertFalse(self.auth_handler.authenticate_user("non_existent", password))
    
    def test_user_login(self):
        """Test user login process"""
        user_id = "test_user"
        password = "test_password"
        
        # Register user first
        self.auth_handler.register_user(user_id, password)
        
        # Create mock form data
        class MockFormData:
            def __init__(self, username, password):
                self.username = username
                self.password = password
        
        form_data = MockFormData(user_id, password)
        
        # Test login
        result = self.auth_handler.login_user(form_data)
        self.assertIsInstance(result, dict)
        self.assertIn("access_token", result)
        self.assertIn("token_type", result)
        self.assertEqual(result["access_token"], user_id)
    
    def test_current_user_from_token(self):
        """Test getting current user from token"""
        user_id = "test_user"
        password = "test_password"
        
        # Register user first
        self.auth_handler.register_user(user_id, password)
        
        # Test valid token (in our simple implementation, token = user_id)
        user_info = self.auth_handler.get_current_user(user_id)
        self.assertEqual(user_info["user_id"], user_id)
        
        # Test invalid token
        with self.assertRaises(Exception):
            self.auth_handler.get_current_user("invalid_token")
    
    def test_user_deletion(self):
        """Test user deletion"""
        user_id = "test_user"
        password = "test_password"
        
        # Register user first
        self.auth_handler.register_user(user_id, password)
        self.assertIn(user_id, self.auth_handler.list_users())
        
        # Delete user
        result = self.auth_handler.delete_user(user_id)
        self.assertTrue(result)
        self.assertNotIn(user_id, self.auth_handler.list_users())
        
        # Try to delete non-existent user
        result = self.auth_handler.delete_user("non_existent")
        self.assertFalse(result)
    
    def test_list_users(self):
        """Test listing users"""
        # Initially empty
        users = self.auth_handler.list_users()
        self.assertEqual(len(users), 0)
        
        # Add some users
        self.auth_handler.register_user("user1", "password1")
        self.auth_handler.register_user("user2", "password2")
        
        users = self.auth_handler.list_users()
        self.assertEqual(len(users), 2)
        self.assertIn("user1", users)
        self.assertIn("user2", users)


class TestAuthServiceInterface(unittest.TestCase):
    """Test the authentication service interface"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Use temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        AUTH_CONFIG['db_path'] = self.temp_db.name
        
        # Create fresh auth service
        global auth_service
        auth_service = auth_service.__class__()
    
    def tearDown(self):
        """Clean up"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_service_registration_and_login(self):
        """Test service registration and login"""
        user_id = "service_test_user"
        password = "service_test_password"
        
        # Register through service
        result = auth_service.register(user_id, password)
        self.assertTrue(result)
        
        # Login through service
        login_result = auth_service.login(user_id, password)
        self.assertIsInstance(login_result, dict)
        self.assertIn("access_token", login_result)
    
    def test_service_health_check(self):
        """Test service health check"""
        health = auth_service.health_check()
        self.assertIsInstance(health, bool)
        self.assertTrue(health)


def run_all_tests():
    """Run all authentication module tests"""
    print("=" * 60)
    print("RUNNING AUTHENTICATION MODULE TESTS")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAuthModule))
    suite.addTests(loader.loadTestsFromTestCase(TestAuthServiceInterface))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ ALL AUTHENTICATION MODULE TESTS PASSED!")
        print("Authentication module is ready for merge to develop branch.")
    else:
        print(f"❌ {len(result.failures)} FAILURE(S), {len(result.errors)} ERROR(S)")
        print("Fix issues before merging to develop branch.")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_all_tests()
