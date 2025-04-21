import os
import tempfile
import unittest
import shutil
import xml.etree.ElementTree as ET
from unittest.mock import patch

from src.metadata.objects import ObjectMetadataGenerator
from src.utils.xml_utils import element_to_string

class TestObjectMetadataGenerator(unittest.TestCase):
    """Tests for the ObjectMetadataGenerator class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create test config
        self.config = {
            "objects": {
                "Custom_Object__c": {
                    "label": "Custom Object",
                    "fields": {
                        "Text_Field__c": {
                            "type": "Text",
                            "length": 255,
                            "required": True
                        },
                        "Number_Field__c": {
                            "type": "Number",
                            "required": False
                        },
                        "Picklist_Field__c": {
                            "type": "Picklist",
                            "values": ["Option 1", "Option 2", "Option 3"]
                        },
                        "Lookup_Field__c": {
                            "type": "Lookup",
                            "referenceTo": "Account"
                        }
                    }
                },
                "Another_Object__c": {
                    "label": "Another Object",
                    "fields": {
                        "Description__c": {
                            "type": "Text",
                            "length": 1000
                        }
                    }
                }
            }
        }
        
        # Initialize generator
        self.generator = ObjectMetadataGenerator(self.config, self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_init(self):
        """Test constructor."""
        self.assertEqual(self.generator.output_dir, self.test_dir)
        self.assertEqual(len(self.generator.object_configs), 2)
    
    def test_generate(self):
        """Test generate method."""
        # Call generate
        count = self.generator.generate()
        
        # Check if object files were created
        objects_dir = os.path.join(self.test_dir, "objects")
        self.assertTrue(os.path.exists(objects_dir), "Objects directory was not created")
        
        # Check object metadata files
        custom_obj_file = os.path.join(objects_dir, "Custom_Object__c.object-meta.xml")
        another_obj_file = os.path.join(objects_dir, "Another_Object__c.object-meta.xml")
        
        self.assertTrue(os.path.exists(custom_obj_file), "Custom object file was not created")
        self.assertTrue(os.path.exists(another_obj_file), "Another object file was not created")
        
        # Check return value
        self.assertEqual(count, 2, "Should create 2 object files")
    
    def test_field_generation(self):
        """Test field metadata generation."""
        # Generate objects
        self.generator.generate()
        
        # Check if field directories were created
        custom_obj_fields_dir = os.path.join(self.test_dir, "objects", "Custom_Object__c", "fields")
        self.assertTrue(os.path.exists(custom_obj_fields_dir), "Fields directory was not created")
        
        # Check field files
        text_field_file = os.path.join(custom_obj_fields_dir, "Text_Field__c.field-meta.xml")
        picklist_field_file = os.path.join(custom_obj_fields_dir, "Picklist_Field__c.field-meta.xml")
        lookup_field_file = os.path.join(custom_obj_fields_dir, "Lookup_Field__c.field-meta.xml")
        
        self.assertTrue(os.path.exists(text_field_file), "Text field file was not created")
        self.assertTrue(os.path.exists(picklist_field_file), "Picklist field file was not created")
        self.assertTrue(os.path.exists(lookup_field_file), "Lookup field file was not created")
    
    def test_object_xml_content(self):
        """Test generated object XML content."""
        # Generate objects
        self.generator.generate()
        
        # Check Custom Object content
        custom_obj_file = os.path.join(self.test_dir, "objects", "Custom_Object__c.object-meta.xml")
        with open(custom_obj_file, 'r') as f:
            content = f.read()
            # Check basic object properties
            self.assertIn("<CustomObject", content)
            self.assertIn("<label>Custom Object</label>", content)
            self.assertIn("<deploymentStatus>Deployed</deploymentStatus>", content)
    
    def test_field_xml_content(self):
        """Test generated field XML content."""
        # Generate objects
        self.generator.generate()
        
        # Check Text field content
        text_field_file = os.path.join(self.test_dir, "objects", "Custom_Object__c", "fields", "Text_Field__c.field-meta.xml")
        with open(text_field_file, 'r') as f:
            content = f.read()
            self.assertIn("<CustomField", content)
            self.assertIn("<fullName>Text_Field__c</fullName>", content)
            self.assertIn("<type>Text</type>", content)
            self.assertIn("<length>255</length>", content)
            self.assertIn("<required>true</required>", content)
        
        # Check Picklist field content
        picklist_field_file = os.path.join(self.test_dir, "objects", "Custom_Object__c", "fields", "Picklist_Field__c.field-meta.xml")
        with open(picklist_field_file, 'r') as f:
            content = f.read()
            self.assertIn("<type>Picklist</type>", content)
            self.assertIn("<valueSet>", content)
            self.assertIn("<fullName>Option 1</fullName>", content)
            self.assertIn("<fullName>Option 2</fullName>", content)
            self.assertIn("<fullName>Option 3</fullName>", content)
        
        # Check Lookup field content
        lookup_field_file = os.path.join(self.test_dir, "objects", "Custom_Object__c", "fields", "Lookup_Field__c.field-meta.xml")
        with open(lookup_field_file, 'r') as f:
            content = f.read()
            self.assertIn("<type>Lookup</type>", content)
            self.assertIn("<referenceTo>Account</referenceTo>", content)
    
    def test_empty_config(self):
        """Test with empty config."""
        # Create generator with empty config
        empty_generator = ObjectMetadataGenerator({"objects": {}}, self.test_dir)
        
        # Generate objects
        count = empty_generator.generate()
        
        # Check results
        self.assertEqual(count, 0, "No object files should be created")