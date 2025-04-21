import os
import tempfile
import unittest
import shutil
import xml.etree.ElementTree as ET
from unittest.mock import patch, MagicMock

from src.metadata.package_builder import PackageBuilder

class TestPackageBuilder(unittest.TestCase):
    """Tests for the PackageBuilder class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Sample metadata types
        self.metadata_types = [
            ('CustomObject', ['Account', 'Contact', 'Opportunity']),
            ('CustomField', ['Account.Custom_Field__c', 'Contact.Email__c']),
            ('Workflow', ['Account_Workflow', 'Contact_Workflow']),
            ('Dashboard', ['Sales_Dashboard', 'Marketing_Dashboard']),
            ('Flow', ['Lead_Process', 'Opportunity_Process'])
        ]
        
        # Initialize builder
        self.builder = PackageBuilder(self.metadata_types)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_init(self):
        """Test constructor."""
        self.assertEqual(self.builder.metadata_types, self.metadata_types)
    
    def test_build_package_xml(self):
        """Test build_package_xml method."""
        # Generate package XML
        package_xml = self.builder.build_package_xml()
        
        # Check if it's a valid XML string
        self.assertTrue(package_xml.startswith('<?xml'))
        self.assertIn('<Package xmlns="http://soap.sforce.com/2006/04/metadata">', package_xml)
        
        # Check if all metadata types are included
        for metadata_type, members in self.metadata_types:
            self.assertIn(f'<name>{metadata_type}</name>', package_xml)
            for member in members:
                self.assertIn(f'<members>{member}</members>', package_xml)
        
        # Check version
        self.assertIn('<version>63.0</version>', package_xml)
    
    def test_save_package_xml(self):
        """Test save_package_xml method."""
        # Define file path
        file_path = os.path.join(self.test_dir, 'package.xml')
        
        # Save package XML
        self.builder.save_package_xml(file_path)
        
        # Check if file exists
        self.assertTrue(os.path.exists(file_path))
        
        # Read file contents
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check content
        self.assertTrue(content.startswith('<?xml'))
        self.assertIn('<Package xmlns="http://soap.sforce.com/2006/04/metadata">', content)
    
    def test_empty_metadata_types(self):
        """Test with empty metadata types."""
        # Create builder with empty metadata types
        empty_builder = PackageBuilder([])
        
        # Generate package XML
        package_xml = empty_builder.build_package_xml()
        
        # Check content
        self.assertIn('<Package xmlns="http://soap.sforce.com/2006/04/metadata">', package_xml)
        self.assertIn('<version>63.0</version>', package_xml)
        self.assertNotIn('<types>', package_xml)
    
    @patch('src.metadata.package_builder.ET')
    def test_element_tree_usage(self, mock_et):
        """Test ElementTree API usage."""
        # Mock objects
        mock_package = MagicMock()
        mock_types = MagicMock()
        mock_member = MagicMock()
        mock_name = MagicMock()
        mock_version = MagicMock()
        
        # Setup mock return values
        mock_et.Element.return_value = mock_package
        mock_et.SubElement.side_effect = [mock_types, mock_member, mock_name, mock_version]
        
        # Create simple builder for testing
        simple_builder = PackageBuilder([('CustomObject', ['Account'])])
        
        # Call method to test
        simple_builder.build_package_xml()
        
        # Verify Element construction
        mock_et.Element.assert_called_once_with('Package', xmlns="http://soap.sforce.com/2006/04/metadata")
        
        # Verify SubElement calls
        mock_et.SubElement.assert_any_call(mock_package, 'types')
        mock_et.SubElement.assert_any_call(mock_types, 'members')
        mock_et.SubElement.assert_any_call(mock_types, 'name')
        mock_et.SubElement.assert_any_call(mock_package, 'version')
    
    def test_main_function(self):
        """Test main function."""
        from src.metadata.package_builder import main
        
        # Use patch to avoid actual file creation
        with patch('src.metadata.package_builder.PackageBuilder.save_package_xml') as mock_save:
            # Call main
            main()
            
            # Verify save_package_xml was called once
            mock_save.assert_called_once()

if __name__ == "__main__":
    unittest.main()