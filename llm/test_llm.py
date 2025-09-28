"""
LLM Module Tests - Test everything in this module

Run this to test all LLM functionality before merging to develop.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm import LLMHandler
from interface import llm_service
from config import PROVIDERS


class TestLLMModule(unittest.TestCase):
    """Test the complete LLM module"""
    
    def test_config_loading(self):
        """Test that configuration loads correctly"""
        self.assertIn('grok', PROVIDERS)
        self.assertIn('api_key_env', PROVIDERS['grok'])
        self.assertIn('base_url', PROVIDERS['grok'])
        self.assertIn('model', PROVIDERS['grok'])
    
    def test_llm_service_interface(self):
        """Test the LLM service interface"""
        self.assertIsNotNone(llm_service)
        self.assertTrue(hasattr(llm_service, 'process_input'))
        self.assertTrue(hasattr(llm_service, 'health_check'))
        self.assertTrue(hasattr(llm_service, 'get_provider'))
    
    @patch.dict(os.environ, {'GROK_API_KEY': 'test_key'})
    def test_llm_handler_initialization(self):
        """Test LLMHandler initialization with mock"""
        try:
            handler = LLMHandler()
            self.assertEqual(handler.provider, 'grok')
            self.assertIsNotNone(handler.api_key)
            self.assertIsNotNone(handler.model)
        except Exception as e:
            self.fail(f"LLMHandler initialization failed: {e}")
    
    @patch.dict(os.environ, {'GROK_API_KEY': 'test_key'})
    @patch('requests.post')
    def test_process_input_storage(self, mock_post):
        """Test processing input for storage"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"summary": "test summary", "tags": ["test", "storage"]}'}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        try:
            handler = LLMHandler()
            result = handler.process_input("test_user", "I like pizza", is_query=False)
            self.assertIsInstance(result, dict)
            mock_post.assert_called_once()
        except Exception as e:
            self.fail(f"process_input for storage failed: {e}")
    
    @patch.dict(os.environ, {'GROK_API_KEY': 'test_key'})
    @patch('requests.post')
    def test_process_input_query(self, mock_post):
        """Test processing input for queries"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"summary": "query summary", "tags": ["test", "query"]}'}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        try:
            handler = LLMHandler()
            result = handler.process_input("test_user", "what do I like?", is_query=True)
            self.assertIsInstance(result, dict)
            mock_post.assert_called_once()
        except Exception as e:
            self.fail(f"process_input for query failed: {e}")
    
    @patch.dict(os.environ, {'GROK_API_KEY': 'test_key'})
    @patch('requests.post')
    def test_natural_language_response(self, mock_post):
        """Test natural language response generation"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "You like pizza."}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        try:
            handler = LLMHandler()
            result = handler.process_input("test_user", "Answer this question: What do I like?", is_query=False)
            self.assertIsInstance(result, str)
            self.assertEqual(result, "You like pizza.")
            mock_post.assert_called_once()
        except Exception as e:
            self.fail(f"natural language response failed: {e}")


class TestIntegrationWithRealAPI(unittest.TestCase):
    """Integration tests with real API (only if keys are available)"""
    
    def setUp(self):
        """Skip if no real API key"""
        if not os.getenv('GROK_API_KEY'):
            self.skipTest("No GROK_API_KEY available for integration tests")
    
    def test_real_llm_health_check(self):
        """Test health check with real API"""
        try:
            health = llm_service.health_check()
            self.assertIsInstance(health, bool)
        except Exception as e:
            self.fail(f"Health check failed: {e}")
    
    def test_real_process_input(self):
        """Test real LLM processing"""
        try:
            # Test storage processing
            result = llm_service.process_input("test_integration_user", "I enjoy reading books", is_query=False)
            self.assertIsNotNone(result)
            
            # Test query processing
            query_result = llm_service.process_input("test_integration_user", "what are my interests?", is_query=True)
            self.assertIsNotNone(query_result)
            
        except Exception as e:
            self.fail(f"Real LLM operation failed: {e}")


def run_all_tests():
    """Run all LLM module tests"""
    print("=" * 60)
    print("RUNNING LLM MODULE TESTS")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLLMModule))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWithRealAPI))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ ALL LLM MODULE TESTS PASSED!")
        print("LLM module is ready for merge to develop branch.")
    else:
        print(f"❌ {len(result.failures)} FAILURE(S), {len(result.errors)} ERROR(S)")
        print("Fix issues before merging to develop branch.")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_all_tests()
