import os
import tempfile
import unittest
import shutil
from unittest.mock import patch, MagicMock

from src.metadata.generator import MetadataGenerator

class TestMetadataGenerator(unittest.TestCase):
    """Tests for the MetadataGenerator class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        
        # Sample config
        self.config = {
            "objects": {
                "Test_Object__c": {
                    "label": "Test Object",
                    "fields": {
                        "Test_Field__c": {"type": "Text"}
                    }
                }
            },
            "workflowRules": {
                "Test_Object__c": {
                    "Test_Rule": {
                        "criteria": "Test_Object__c.Test_Field__c = 'Test'"
                    }
                }
            },
            "dashboards": {
                "Test_Dashboard": {
                    "label": "Test Dashboard"
                }
            },
            "flows": {
                "Test_Flow": {
                    "description": "Test Flow"
                }
            }
        }
        
        # API version for testing
        self.api_version = "56.0"
        
        # Initialize generator
        self.generator = MetadataGenerator(self.config, self.test_dir, self.api_version)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_init(self):
        """Test constructor."""
        # Check properties
        self.assertEqual(self.generator.output_dir, self.test_dir)
        self.assertEqual(self.generator.deploy_dir, self.test_dir)  # Alias for backward compatibility
        self.assertEqual(self.generator.api_version, self.api_version)
        
        # Check components initialization
        self.assertIsNotNone(self.generator.object_generator)
        self.assertIsNotNone(self.generator.workflow_generator)
        self.assertIsNotNone(self.generator.dashboard_generator)
        self.assertIsNotNone(self.generator.flow_generator)
        self.assertIsNotNone(self.generator.package_generator)
        
        # Check directory creation
        metadata_dir = os.path.join(self.test_dir, "force-app", "main", "default")
        self.assertTrue(os.path.exists(metadata_dir), "Metadata directory was not created")
    
    def test_generate_all(self):
        """Test generate_all method."""
        # Mock component generators
        self.generator.object_generator.generate = MagicMock(return_value=1)
        self.generator.workflow_generator.generate = MagicMock(return_value=1)
        self.generator.dashboard_generator.generate = MagicMock(return_value=1)
        self.generator.flow_generator.generate = MagicMock(return_value=1)
        self.generator.package_generator.generate = MagicMock(return_value=True)
        
        # Set stats for mocked generators
        self.generator.object_generator.stats = {"fields_created": 2}
        self.generator.workflow_generator.stats = {"rules_created": 1}
        
        # Call generate_all
        stats = self.generator.generate_all()
        
        # Check if component generators were called
        self.generator.object_generator.generate.assert_called_once()
        self.generator.workflow_generator.generate.assert_called_once()
        self.generator.dashboard_generator.generate.assert_called_once()
        self.generator.flow_generator.generate.assert_called_once()
        self.generator.package_generator.generate.assert_called_once()
        
        # Check stats
        self.assertEqual(stats["objects_processed"], 1)
        self.assertEqual(stats["fields_created"], 2)
        self.assertEqual(stats["workflow_rules_created"], 1)
        self.assertEqual(stats["dashboards_created"], 1)
        self.assertEqual(stats["flows_created"], 1)
    
    def test_get_stats(self):
        """Test get_stats method."""
        # Set some stats
        self.generator.stats = {
            "objects_processed": 5,
            "fields_created": 10
        }
        
        # Get stats
        stats = self.generator.get_stats()
        
        # Check stats
        self.assertEqual(stats["objects_processed"], 5)
        self.assertEqual(stats["fields_created"], 10)
    
    def test_get_metadata_dir(self):
        """Test get_metadata_dir method."""
        metadata_dir = self.generator.get_metadata_dir()
        expected_dir = os.path.join(self.test_dir, "force-app", "main", "default")
        self.assertEqual(metadata_dir, expected_dir)

if __name__ == "__main__":
    unittest.main()