import os
import tempfile
import unittest
from unittest.mock import patch, mock_open

from src.config.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    
    def setUp(self):
        # Create temporary files for testing
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.json')
        self.env_file = os.path.join(self.temp_dir, 'test.env')
        
        # Sample config and env content
        self.config_content = """
        {
            "objects": {
                "Test_Object__c": {
                    "label": "Test Object",
                    "fields": [
                        {"name": "Test_Field__c", "type": "Text"}
                    ]
                }
            }
        }
        """
        
        self.env_content = """
        SF_USERNAME=test@example.com
        SF_PASSWORD=password123
        SF_SECURITY_TOKEN=abcdef
        SF_INSTANCE_URL=https://test.salesforce.com
        """
        
        # Write files
        with open(self.config_file, 'w') as f:
            f.write(self.config_content)
            
        with open(self.env_file, 'w') as f:
            f.write(self.env_content)
        
    def tearDown(self):
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir)
        
    @patch.dict('os.environ', {}, clear=True)
    def test_load_environment(self):
        """Test loading environment variables from .env file."""
        config_loader = ConfigLoader(self.config_file, self.env_file)
        config_loader.load_environment()
        
        # Check if environment variables were loaded
        self.assertEqual(os.environ.get('SF_USERNAME'), 'test@example.com')
        self.assertEqual(os.environ.get('SF_PASSWORD'), 'password123')
        self.assertEqual(os.environ.get('SF_SECURITY_TOKEN'), 'abcdef')
        self.assertEqual(os.environ.get('SF_INSTANCE_URL'), 'https://test.salesforce.com')
        
    @patch.dict('os.environ', {'SF_USERNAME': 'test@example.com', 'SF_PASSWORD': 'password123'})
    def test_validate_environment_variables_success(self):
        """Test successful validation of environment variables."""
        config_loader = ConfigLoader(self.config_file, self.env_file)
        
        # This should not raise an error
        config_loader._validate_environment_variables()
        
    @patch.dict('os.environ', {'SF_USERNAME': 'test@example.com'}, clear=True)
    def test_validate_environment_variables_failure(self):
        """Test validation of environment variables with missing variables."""
        config_loader = ConfigLoader(self.config_file, self.env_file)
        
        # This should raise a ValueError
        with self.assertRaises(ValueError):
            config_loader._validate_environment_variables()


if __name__ == "__main__":
    unittest.main()