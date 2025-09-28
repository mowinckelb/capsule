"""
Web Module Tests - Test everything in this module

Run this to test all web functionality before merging to develop.
"""

import os
import sys
import unittest
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface import web_service


class TestWebModule(unittest.TestCase):
    """Test the complete web module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.web_dir = Path(__file__).parent
    
    def test_web_service_interface(self):
        """Test the web service interface"""
        self.assertIsNotNone(web_service)
        self.assertTrue(hasattr(web_service, 'get_static_files'))
        self.assertTrue(hasattr(web_service, 'get_main_interface'))
        self.assertTrue(hasattr(web_service, 'health_check'))
    
    def test_static_files_discovery(self):
        """Test that static files are discovered correctly"""
        static_files = web_service.get_static_files()
        self.assertIsInstance(static_files, dict)
        
        # Check that main files are discovered
        file_names = list(static_files.keys())
        self.assertIn('interface', file_names)  # interface.html
        self.assertIn('app', file_names)        # app.js
        self.assertIn('config', file_names)     # config.js
    
    def test_main_interface_file(self):
        """Test that main interface file exists and is accessible"""
        interface_path = web_service.get_main_interface()
        self.assertIsNotNone(interface_path)
        self.assertTrue(os.path.exists(interface_path))
        
        # Check that file has content
        content = web_service.read_file('interface.html')
        self.assertIsNotNone(content)
        self.assertIn('<!DOCTYPE html>', content)
        self.assertIn('Capsule', content)
    
    def test_app_js_file(self):
        """Test that app.js file exists and is accessible"""
        app_js_path = web_service.get_app_js()
        self.assertIsNotNone(app_js_path)
        self.assertTrue(os.path.exists(app_js_path))
        
        # Check that file has content
        content = web_service.read_file('app.js')
        self.assertIsNotNone(content)
        self.assertIn('CapsuleApp', content)
        self.assertIn('class', content)
    
    def test_config_js_file(self):
        """Test that config.js file exists and is accessible"""
        config_js_path = web_service.get_config_js()
        self.assertIsNotNone(config_js_path)
        self.assertTrue(os.path.exists(config_js_path))
        
        # Check that file has content
        content = web_service.read_file('config.js')
        self.assertIsNotNone(content)
        self.assertIn('WEB_CONFIG', content)
    
    def test_file_reading(self):
        """Test reading file contents"""
        # Test reading existing file
        content = web_service.read_file('interface.html')
        self.assertIsNotNone(content)
        self.assertIsInstance(content, str)
        
        # Test reading non-existent file
        no_content = web_service.read_file('nonexistent.html')
        self.assertIsNone(no_content)
    
    def test_health_check(self):
        """Test web service health check"""
        health = web_service.health_check()
        self.assertIsInstance(health, bool)
        self.assertTrue(health)  # Should be healthy if files exist
    
    def test_file_info(self):
        """Test getting file information"""
        info = web_service.get_file_info()
        self.assertIsInstance(info, dict)
        
        # Check required fields
        self.assertIn('total_files', info)
        self.assertIn('files', info)
        self.assertIn('main_interface', info)
        self.assertIn('app_js', info)
        
        # Check values
        self.assertGreater(info['total_files'], 0)
        self.assertTrue(info['main_interface'])
        self.assertTrue(info['app_js'])
    
    def test_serve_directory(self):
        """Test getting serve directory"""
        serve_dir = web_service.serve_directory()
        self.assertIsInstance(serve_dir, str)
        self.assertTrue(os.path.exists(serve_dir))
        self.assertTrue(os.path.isdir(serve_dir))


class TestWebFiles(unittest.TestCase):
    """Test the actual web files"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.web_dir = Path(__file__).parent
    
    def test_html_structure(self):
        """Test HTML file structure"""
        content = web_service.read_file('interface.html')
        self.assertIsNotNone(content)
        
        # Check basic HTML structure
        self.assertIn('<!DOCTYPE html>', content)
        self.assertIn('<html>', content)
        self.assertIn('<head>', content)
        self.assertIn('<body>', content)
        
        # Check for required elements
        self.assertIn('auth-section', content)
        self.assertIn('app-section', content)
        self.assertIn('app.js', content)
        
        # Check for form elements
        self.assertIn('login-user', content)
        self.assertIn('memory-input', content)
        self.assertIn('query-input', content)
    
    def test_javascript_structure(self):
        """Test JavaScript file structure"""
        content = web_service.read_file('app.js')
        self.assertIsNotNone(content)
        
        # Check for main class and methods
        self.assertIn('class CapsuleApp', content)
        self.assertIn('constructor()', content)
        self.assertIn('login()', content)
        self.assertIn('register()', content)
        self.assertIn('addMemory()', content)
        self.assertIn('queryMemories()', content)
        
        # Check for API interaction
        self.assertIn('makeRequest', content)
        self.assertIn('fetch(', content)
    
    def test_config_structure(self):
        """Test configuration file structure"""
        content = web_service.read_file('config.js')
        self.assertIsNotNone(content)
        
        # Check for main config object
        self.assertIn('WEB_CONFIG', content)
        
        # Check for required sections
        self.assertIn('api:', content)
        self.assertIn('ui:', content)
        self.assertIn('features:', content)
        self.assertIn('storage:', content)
        self.assertIn('messages:', content)
    
    def test_css_styling(self):
        """Test CSS styling in HTML"""
        content = web_service.read_file('interface.html')
        self.assertIsNotNone(content)
        
        # Check for CSS variables and styling
        self.assertIn(':root {', content)
        self.assertIn('--primary-color:', content)
        self.assertIn('.container', content)
        self.assertIn('.card', content)
        self.assertIn('.btn', content)


def run_all_tests():
    """Run all web module tests"""
    print("=" * 60)
    print("RUNNING WEB MODULE TESTS")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWebModule))
    suite.addTests(loader.loadTestsFromTestCase(TestWebFiles))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ ALL WEB MODULE TESTS PASSED!")
        print("Web module is ready for merge to develop branch.")
    else:
        print(f"❌ {len(result.failures)} FAILURE(S), {len(result.errors)} ERROR(S)")
        print("Fix issues before merging to develop branch.")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_all_tests()
