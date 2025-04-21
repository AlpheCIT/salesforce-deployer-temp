import os
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch, MagicMock

from src.metadata.generator import MetadataGenerator
from src.metadata.objects import ObjectMetadataGenerator
from src.metadata.workflows import WorkflowMetadataGenerator
from src.metadata.dashboards import DashboardMetadataGenerator
from src.metadata.flows import FlowMetadataGenerator
from src.metadata.package import PackageGenerator
from src.utils.xml_utils import patch_xml_writing


class TestMetadataGenerators(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Initialize sample config with proper structure
        self.sample_config = {
            "objects": {
                "Test_Object__c": {
                    "label": "Test Object",
                    "fields": {
                        "Test_Field__c": {"type": "Text", "length": 255},
                        "Picklist_Field__c": {"type": "Picklist", "values": ["Value1", "Value2", "Value3"]},
                        "Lookup_Field__c": {"type": "Lookup", "referenceTo": "Another_Object__c"}
                    }
                }
            },
            "workflowRules": {
                "Test_Object__c": {
                    "Test_Object_Rule": {
                        "description": "Test Workflow Rule",
                        "criteria": "Test_Object__c.Test_Field__c = 'Test'",
                        "active": True
                    }
                }
            },
            "dashboards": {
                "Test_Dashboard": {
                    "label": "Test Dashboard",
                    "charts": [{"type": "Bar", "title": "Test Chart", "report": "Test_Report"}]
                }
            },
            "flows": {
                "Test_Flow": {
                    "description": "Test Flow Description",
                    "status": "Active"
                }
            }
        }
        
        # Initialize all required generators
        self.object_generator = ObjectMetadataGenerator(self.sample_config, self.test_dir)
        self.workflow_generator = WorkflowMetadataGenerator(self.sample_config, self.test_dir)
        self.dashboard_generator = DashboardMetadataGenerator(self.sample_config, self.test_dir)
        self.flow_generator = FlowMetadataGenerator(self.sample_config, self.test_dir)
        self.package_generator = PackageGenerator(self.sample_config, self.test_dir, "56.0")
        
        # Apply XML patch for safety
        from src.utils.xml_utils import patch_xml_writing
        self.xml_patcher = patch_xml_writing()
        self.xml_patcher.__enter__()

    def tearDown(self):
        """Clean up test environment."""
        # Remove the XML writing patch
        self.xml_patcher.__exit__(None, None, None)
        shutil.rmtree(self.test_dir)
        
    def test_object_generation(self):
        """Test that object metadata files are generated correctly."""
        # Generate object metadata
        self.object_generator.generate()
        
        # Check if object metadata file was created
        object_file = os.path.join(self.test_dir, "objects", "Test_Object__c.object-meta.xml")
        self.assertTrue(os.path.exists(object_file), "Object metadata file was not created")
        
        # Check file contents
        with open(object_file, 'r') as f:
            content = f.read()
            self.assertIn("<CustomObject", content)
            self.assertIn("<label>Test Object</label>", content)
            
        # Check if field files were created
        fields_dir = os.path.join(self.test_dir, "objects", "Test_Object__c", "fields")
        self.assertTrue(os.path.exists(fields_dir), "Fields directory was not created")
        
        # Check if specific field files exist
        text_field_file = os.path.join(fields_dir, "Test_Field__c.field-meta.xml")
        picklist_field_file = os.path.join(fields_dir, "Picklist_Field__c.field-meta.xml")
        lookup_field_file = os.path.join(fields_dir, "Lookup_Field__c.field-meta.xml")
        
        self.assertTrue(os.path.exists(text_field_file), "Text field metadata file was not created")
        self.assertTrue(os.path.exists(picklist_field_file), "Picklist field metadata file was not created")
        self.assertTrue(os.path.exists(lookup_field_file), "Lookup field metadata file was not created")
        
        # Check field file contents
        with open(text_field_file, 'r') as f:
            content = f.read()
            self.assertIn("<CustomField", content)
            self.assertIn("<fullName>Test_Field__c</fullName>", content)
            self.assertIn("<type>Text</type>", content)
            
        with open(picklist_field_file, 'r') as f:
            content = f.read()
            self.assertIn("<type>Picklist</type>", content)
            self.assertIn("<valueSet>", content)
            self.assertIn("<value>", content)
            self.assertIn("Value1", content)
            self.assertIn("Value2", content)
            
        with open(lookup_field_file, 'r') as f:
            content = f.read()
            self.assertIn("<type>Lookup</type>", content)
            self.assertIn("<referenceTo>Another_Object__c</referenceTo>", content)
            
    def test_workflow_generation(self):
        """Test that workflow metadata files are generated correctly."""
        # Generate workflow metadata
        count = self.workflow_generator.generate()
        
        # Check if workflow file was created (print all the files in the directory for debugging)
        workflow_dir = os.path.join(self.test_dir, "workflows")
        self.assertTrue(os.path.exists(workflow_dir), "Workflows directory was not created")
        
        print(f"Files in workflow directory: {os.listdir(workflow_dir) if os.path.exists(workflow_dir) else 'Directory does not exist'}")
        
        # Should be one file for Test_Object__c
        workflow_file = os.path.join(workflow_dir, "Test_Object__c.workflow-meta.xml")
        self.assertTrue(os.path.exists(workflow_file), f"Workflow file not found at {workflow_file}")
        
        # Check file contents
        with open(workflow_file, 'r') as f:
            content = f.read()
            self.assertIn("<Workflow", content)
            self.assertIn("<fullName>Test_Object_Rule</fullName>", content)
            self.assertIn("<description>Test Workflow Rule</description>", content)
            self.assertIn("<formula>Test_Object__c.Test_Field__c = 'Test'</formula>", content)
            
    def test_dashboard_generation(self):
        """Test that dashboard metadata files are generated correctly."""
        # Generate dashboard metadata
        count = self.dashboard_generator.generate()
        
        # Check if dashboard directory and file were created
        dashboard_dir = os.path.join(self.test_dir, "dashboards")
        self.assertTrue(os.path.exists(dashboard_dir), "Dashboards directory was not created")
        
        # Check for the dashboard file
        dashboard_file = os.path.join(dashboard_dir, "Test_Dashboard.dashboard-meta.xml")
        self.assertTrue(os.path.exists(dashboard_file), f"Dashboard file not found at {dashboard_file}")
        
        # Dashboard files should be created
        self.assertEqual(count, 1, "Should create 1 dashboard")
        
        # Check file contents
        with open(dashboard_file, 'r') as f:
            content = f.read()
            self.assertIn("<Dashboard", content)
            self.assertIn("<label>Test Dashboard</label>", content)
            self.assertIn("<title>Test Chart</title>", content)
            self.assertIn("<report>Test_Report</report>", content)
            
    def test_flow_generation(self):
        """Test that flow metadata files are generated correctly."""
        # Generate flow metadata
        self.flow_generator.generate()
        
        # Check if flow metadata file was created
        flow_file = os.path.join(self.test_dir, "flows", "Test_Flow.flow-meta.xml")
        self.assertTrue(os.path.exists(flow_file), "Flow metadata file was not created")
        
        # Check file contents
        with open(flow_file, 'r') as f:
            content = f.read()
            self.assertIn("<Flow", content)
            self.assertIn("<description>Test Flow Description</description>", content)
            
    def test_package_generation(self):
        """Test that package.xml is generated correctly."""
        # Generate package.xml
        self.package_generator.generate()
        
        # Check if package.xml file was created
        package_file = os.path.join(self.test_dir, "manifest", "package.xml")
        self.assertTrue(os.path.exists(package_file), "package.xml file was not created")
        
        # Check file contents
        with open(package_file, 'r') as f:
            content = f.read()
            self.assertIn("<Package", content)
            self.assertIn("<version>56.0</version>", content)
            self.assertIn("<name>CustomObject</name>", content)
            self.assertIn("<members>Test_Object__c</members>", content)
            
    def test_full_metadata_generation(self):
        """Test the full metadata generation process through the MetadataGenerator class."""
        # Initialize the metadata generator
        metadata_generator = MetadataGenerator(self.sample_config, self.test_dir, "56.0")
        
        # Generate all metadata
        metadata_generator.generate_all()
        
        # Check if basic directories exist with correct structure
        dirs_to_check = [
            os.path.join(self.test_dir, "force-app", "main", "default", "objects"),
            os.path.join(self.test_dir, "force-app", "main", "default", "workflows"),
            os.path.join(self.test_dir, "force-app", "main", "default", "dashboards"),
            os.path.join(self.test_dir, "force-app", "main", "default", "flows"),
            os.path.join(self.test_dir, "manifest")
        ]
        
        for dir_path in dirs_to_check:
            self.assertTrue(os.path.exists(dir_path), f"Directory {dir_path} was not created")
            
        # Check if package.xml was created
        package_file = os.path.join(self.test_dir, "manifest", "package.xml")
        self.assertTrue(os.path.exists(package_file), "package.xml file was not created")
        
        # Check stats
        stats = metadata_generator.get_stats()
        self.assertGreater(stats.get("objects_processed", 0), 0)
        self.assertGreater(stats.get("fields_created", 0), 0)


if __name__ == "__main__":
    unittest.main()