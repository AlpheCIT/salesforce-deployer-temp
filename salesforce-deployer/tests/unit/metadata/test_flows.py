import os
import tempfile
import unittest
import shutil
import xml.etree.ElementTree as ET
from unittest.mock import patch

from src.metadata.flows import FlowMetadataGenerator
from src.utils.xml_utils import element_to_string

class TestFlowMetadataGenerator(unittest.TestCase):
    """Tests for the FlowMetadataGenerator class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create test config
        self.config = {
            "flows": {
                "Account_Creation": {
                    "description": "Flow for creating accounts",
                    "status": "Active",
                    "label": "Account Creation Flow"
                },
                "Lead_Conversion": {
                    "description": "Flow for lead conversion process",
                    "status": "Draft"
                }
            }
        }
        
        # Initialize generator
        self.generator = FlowMetadataGenerator(self.config, self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_init(self):
        """Test constructor."""
        self.assertEqual(self.generator.metadata_dir, self.test_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "flows")))
        self.assertEqual(len(self.generator.flow_configs), 2)
    
    def test_generate(self):
        """Test generate method."""
        # Call generate
        count = self.generator.generate()
        
        # Check if flow files were created
        account_file = os.path.join(self.test_dir, "flows", "Account_Creation.flow-meta.xml")
        lead_file = os.path.join(self.test_dir, "flows", "Lead_Conversion.flow-meta.xml")
        
        self.assertTrue(os.path.exists(account_file), "Account flow file was not created")
        self.assertTrue(os.path.exists(lead_file), "Lead flow file was not created")
        
        # Check return value
        self.assertEqual(count, 2, "Should create 2 flow files")
    
    def test_flow_xml_content(self):
        """Test generated XML content."""
        # Generate flows
        self.generator.generate()
        
        # Check Account flow content
        account_file = os.path.join(self.test_dir, "flows", "Account_Creation.flow-meta.xml")
        with open(account_file, 'r') as f:
            content = f.read()
            # Check basic flow properties
            self.assertIn("<Flow", content)
            self.assertIn("<apiVersion>56.0</apiVersion>", content)
            self.assertIn("<description>Flow for creating accounts</description>", content)
            self.assertIn("<status>Active</status>", content)
            self.assertIn("<label>Account Creation Flow</label>", content)
    
    def test_default_values(self):
        """Test default values in generated XML."""
        # Generate flows
        self.generator.generate()
        
        # Check Lead flow content with defaults
        lead_file = os.path.join(self.test_dir, "flows", "Lead_Conversion.flow-meta.xml")
        with open(lead_file, 'r') as f:
            content = f.read()
            self.assertIn("<label>Lead Conversion</label>", content)  # Default label from name
            self.assertIn("<status>Draft</status>", content)  # Specified status
    
    def test_empty_config(self):
        """Test with empty config."""
        # Create generator with empty config
        empty_generator = FlowMetadataGenerator({"flows": {}}, self.test_dir)
        
        # Generate flows
        count = empty_generator.generate()
        
        # Check results
        self.assertEqual(count, 0, "No flow files should be created")
        self.assertEqual(len(os.listdir(os.path.join(self.test_dir, "flows"))), 0)

if __name__ == "__main__":
    unittest.main()