import unittest
import os
import tempfile
import json
from unittest.mock import patch, MagicMock

from src.utils.version_manager import ApiVersionManager


class TestVersionManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.test_dir, 'api_versions.json')
        
        # Sample version configuration
        self.version_config = {
            "default": "56.0",
            "supported": [
                {"version": "56.0", "releaseDate": "2022-10-15", "endOfSupportDate": "2023-10-15"},
                {"version": "55.0", "releaseDate": "2022-06-15", "endOfSupportDate": "2023-06-15"},
                {"version": "54.0", "releaseDate": "2022-02-15", "endOfSupportDate": "2023-02-15"}
            ],
            "metadataTypeAvailability": {
                "Flow": "18.0+",
                "LightningComponentBundle": "45.0+"
            }
        }
        
        # Write config file
        with open(self.config_path, 'w') as f:
            json.dump(self.version_config, f)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_get_default_version(self):
        """Test getting default API version."""
        version_manager = ApiVersionManager(self.config_path)
        default_version = version_manager.get_default_version()
        
        self.assertEqual(default_version, "56.0")
    
    def test_get_latest_version(self):
        """Test getting latest API version."""
        version_manager = ApiVersionManager(self.config_path)
        latest_version = version_manager.get_latest_version()
        
        self.assertEqual(latest_version, "56.0")
    
    def test_is_supported(self):
        """Test checking if a version is supported."""
        version_manager = ApiVersionManager(self.config_path)
        
        self.assertTrue(version_manager.is_supported("56.0"))
        self.assertTrue(version_manager.is_supported("55.0"))
        self.assertFalse(version_manager.is_supported("57.0"))
        self.assertFalse(version_manager.is_supported("invalid"))
    
    def test_check_metadata_compatibility(self):
        """Test checking metadata compatibility with versions."""
        version_manager = ApiVersionManager(self.config_path)
        
        # Flow should be compatible with version 56.0
        self.assertTrue(version_manager.check_metadata_compatibility("Flow", "56.0"))
        
        # Flow should not be compatible with version 17.0
        self.assertFalse(version_manager.check_metadata_compatibility("Flow", "17.0"))
        
        # Unknown metadata type should be considered compatible
        self.assertTrue(version_manager.check_metadata_compatibility("UnknownType", "56.0"))
    
    @patch('requests.get')
    def test_fetch_available_versions(self, mock_get):
        """Test fetching available versions from Salesforce."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"version": "57.0", "label": "Winter '23", "url": "/services/data/v57.0"},
            {"version": "56.0", "label": "Summer '22", "url": "/services/data/v56.0"},
            {"version": "55.0", "label": "Spring '22", "url": "/services/data/v55.0"}
        ]
        mock_get.return_value = mock_response
        
        # Fetch versions
        version_manager = ApiVersionManager(self.config_path)
        versions = version_manager.fetch_available_versions(
            "https://test.salesforce.com", "test_token"
        )
        
        # Verify request and response
        mock_get.assert_called_once()
        self.assertEqual(len(versions), 3)
        self.assertEqual(versions[0]["version"], "57.0")


if __name__ == "__main__":
    unittest.main()