"""
LLM Module Tests

These tests ensure the LLM module works correctly in isolation.
Run these tests whenever you modify the LLM implementation.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.interface import LLMService, LLMInterface
from llm.grok_implementation import GrokLLMImplementation


class MockLLMImplementation(LLMInterface):
    """Mock LLM implementation for testing"""
    
    def process_input(self, user_id: str, input_text, is_query: bool = False, context: str = None):
        if is_query:
            return {"summary": f"Query for {user_id}", "tags": ["test", "query"]}
        elif "Answer this question:" in str(input_text):
            return "Mock natural language response"
        else:
            return {"summary": f"Storage for {user_id}", "tags": ["test", "storage"]}
    
    def health_check(self) -> bool:
        return True
    
    def get_provider_info(self) -> Dict[str, str]:
        return {"provider": "mock", "status": "healthy"}


class TestLLMInterface(unittest.TestCase):
    """Test the LLM interface and service"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.llm_service = LLMService()
        self.mock_impl = MockLLMImplementation()
        self.llm_service.initialize(self.mock_impl)
    
    def test_service_initialization(self):
        """Test that LLM service initializes correctly"""
        self.assertIsNotNone(self.llm_service._llm_implementation)
        self.assertTrue(self.llm_service.health_check())
    
    def test_storage_processing(self):
        """Test processing input for storage"""
        result = self.llm_service.process_input(
            user_id="test_user",
            input_text="I like pizza",
            is_query=False
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("summary", result)
        self.assertIn("tags", result)
        self.assertEqual(result["summary"], "Storage for test_user")
    
    def test_query_processing(self):
        """Test processing input for queries"""
        result = self.llm_service.process_input(
            user_id="test_user",
            input_text="what do I like?",
            is_query=True
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("summary", result)
        self.assertIn("tags", result)
        self.assertEqual(result["summary"], "Query for test_user")
    
    def test_natural_language_response(self):
        """Test natural language response generation"""
        result = self.llm_service.process_input(
            user_id="test_user",
            input_text="Answer this question: what do I like?",
            is_query=False
        )
        
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Mock natural language response")
    
    def test_health_check(self):
        """Test health check functionality"""
        self.assertTrue(self.llm_service.health_check())
    
    def test_provider_info(self):
        """Test getting provider information"""
        info = self.llm_service.get_info()
        self.assertIsInstance(info, dict)
        self.assertIn("provider", info)
        self.assertEqual(info["provider"], "mock")


class TestGrokImplementation(unittest.TestCase):
    """Test Grok-specific implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Skip these tests if no API key is available
        if not os.getenv('GROK_API_KEY'):
            self.skipTest("GROK_API_KEY not available")
        
        self.grok_impl = GrokLLMImplementation()
    
    def test_initialization(self):
        """Test Grok implementation initializes correctly"""
        self.assertIsNotNone(self.grok_impl.api_key)
        self.assertEqual(self.grok_impl.model, 'grok-4')
    
    def test_provider_info(self):
        """Test getting Grok provider information"""
        info = self.grok_impl.get_provider_info()
        self.assertEqual(info["provider"], "grok")
        self.assertEqual(info["model"], "grok-4")
        self.assertEqual(info["api_key_status"], "configured")
    
    @patch('requests.post')
    def test_successful_api_call(self, mock_post):
        """Test successful API call to Grok"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"summary": "test", "tags": ["test"]}'}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = self.grok_impl.process_input(
            user_id="test",
            input_text="test input",
            is_query=False
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("summary", result)
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_health_check(self, mock_post):
        """Test health check functionality"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        self.assertTrue(self.grok_impl.health_check())
        mock_post.assert_called_once()


def run_llm_tests():
    """Run all LLM module tests"""
    print("=" * 50)
    print("Running LLM Module Tests")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLLMInterface))
    suite.addTests(loader.loadTestsFromTestCase(TestGrokImplementation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✓ All LLM module tests passed!")
    else:
        print(f"✗ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
    print("=" * 50)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_llm_tests()
