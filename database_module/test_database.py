"""
Database Module Tests - Test everything in this module

Run this to test all database functionality before merging to develop.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DBHandler
from interface import database_service
from config import DB_PROVIDERS


class TestDatabaseModule(unittest.TestCase):
    """Test the complete database module"""
    
    def test_config_loading(self):
        """Test that configuration loads correctly"""
        self.assertIn('pinecone', DB_PROVIDERS)
        self.assertIn('api_key_env', DB_PROVIDERS['pinecone'])
        self.assertIn('index_name', DB_PROVIDERS['pinecone'])
    
    def test_database_service_interface(self):
        """Test the database service interface"""
        self.assertIsNotNone(database_service)
        self.assertTrue(hasattr(database_service, 'add_memory'))
        self.assertTrue(hasattr(database_service, 'query_memories'))
        self.assertTrue(hasattr(database_service, 'health_check'))
    
    @patch.dict(os.environ, {'PINECONE_API_KEY': 'test_key'})
    @patch('database.Pinecone')
    @patch('database.SentenceTransformer')
    def test_db_handler_initialization(self, mock_transformer, mock_pinecone):
        """Test DBHandler initialization with mocks"""
        # Mock the dependencies
        mock_pinecone_instance = Mock()
        mock_pinecone.return_value = mock_pinecone_instance
        mock_pinecone_instance.list_indexes.return_value.names.return_value = []
        
        mock_transformer_instance = Mock()
        mock_transformer.return_value = mock_transformer_instance
        
        try:
            db = DBHandler()
            self.assertEqual(db.provider, 'pinecone')
            self.assertIsNotNone(db.pc)
            self.assertIsNotNone(db.model)
        except Exception as e:
            self.fail(f"DBHandler initialization failed: {e}")
    
    @patch.dict(os.environ, {'PINECONE_API_KEY': 'test_key'})
    @patch('database.Pinecone')
    @patch('database.SentenceTransformer')
    def test_add_memory_string(self, mock_transformer, mock_pinecone):
        """Test adding string memory"""
        # Setup mocks
        mock_pinecone_instance = Mock()
        mock_pinecone.return_value = mock_pinecone_instance
        mock_index = Mock()
        mock_pinecone_instance.Index.return_value = mock_index
        mock_pinecone_instance.list_indexes.return_value.names.return_value = ['test-index']
        
        mock_transformer_instance = Mock()
        mock_transformer_instance.encode.return_value.tolist.return_value = [0.1, 0.2, 0.3]
        mock_transformer.return_value = mock_transformer_instance
        
        try:
            db = DBHandler()
            db.add_memory("test_user", "I like pizza")
            mock_index.upsert.assert_called_once()
        except Exception as e:
            self.fail(f"add_memory failed: {e}")
    
    @patch.dict(os.environ, {'PINECONE_API_KEY': 'test_key'})
    @patch('database.Pinecone')
    @patch('database.SentenceTransformer')
    def test_query_memories(self, mock_transformer, mock_pinecone):
        """Test querying memories"""
        # Setup mocks
        mock_pinecone_instance = Mock()
        mock_pinecone.return_value = mock_pinecone_instance
        mock_index = Mock()
        mock_pinecone_instance.Index.return_value = mock_index
        mock_pinecone_instance.list_indexes.return_value.names.return_value = ['test-index']
        
        # Mock query results
        mock_match = Mock()
        mock_match.metadata = {"memory": "I like pizza"}
        mock_result = Mock()
        mock_result.matches = [mock_match]
        mock_index.query.return_value = mock_result
        
        mock_transformer_instance = Mock()
        mock_transformer_instance.encode.return_value.tolist.return_value = [0.1, 0.2, 0.3]
        mock_transformer.return_value = mock_transformer_instance
        
        try:
            db = DBHandler()
            results = db.query_memories("test_user", "food")
            self.assertIsInstance(results, list)
            mock_index.query.assert_called_once()
        except Exception as e:
            self.fail(f"query_memories failed: {e}")


class TestIntegrationWithRealAPI(unittest.TestCase):
    """Integration tests with real API (only if keys are available)"""
    
    def setUp(self):
        """Skip if no real API key"""
        if not os.getenv('PINECONE_API_KEY'):
            self.skipTest("No PINECONE_API_KEY available for integration tests")
    
    def test_real_database_health_check(self):
        """Test health check with real API"""
        try:
            health = database_service.health_check()
            self.assertIsInstance(health, bool)
        except Exception as e:
            self.fail(f"Health check failed: {e}")
    
    def test_real_add_and_query(self):
        """Test real add and query operation"""
        try:
            # Add a test memory
            database_service.add_memory("test_integration_user", "Integration test memory")
            
            # Query for it
            results = database_service.query_memories("test_integration_user", "integration test")
            self.assertIsInstance(results, list)
            
        except Exception as e:
            self.fail(f"Real database operation failed: {e}")


def run_all_tests():
    """Run all database module tests"""
    print("=" * 60)
    print("RUNNING DATABASE MODULE TESTS")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseModule))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWithRealAPI))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ ALL DATABASE MODULE TESTS PASSED!")
        print("Database module is ready for merge to develop branch.")
    else:
        print(f"❌ {len(result.failures)} FAILURE(S), {len(result.errors)} ERROR(S)")
        print("Fix issues before merging to develop branch.")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_all_tests()
