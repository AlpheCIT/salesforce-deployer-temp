import os
import tempfile
import unittest
import shutil
import xml.etree.ElementTree as ET
from unittest.mock import patch

from src.metadata.dashboards import DashboardMetadataGenerator
from src.utils.xml_utils import element_to_string

class TestDashboardMetadataGenerator(unittest.TestCase):
    """Tests for the DashboardMetadataGenerator class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create test config
        self.config = {
            "dashboards": {
                "Sales_Dashboard": {
                    "label": "Sales Dashboard",
                    "folder": "My_Dashboards",
                    "charts": [
                        {
                            "type": "Bar",
                            "title": "Revenue by Quarter",
                            "report": "Sales_Report"
                        },
                        {
                            "type": "Pie",
                            "title": "Deals by Stage",
                            "report": "Pipeline_Report"
                        }
                    ]
                },
                "Marketing_Dashboard": {
                    "label": "Marketing Dashboard",
                    "charts": [
                        {
                            "type": "Line",
                            "title": "Campaign Performance",
                            "report": "Marketing_Report"
                        }
                    ]
                }
            }
        }
        
        # Initialize generator
        self.generator = DashboardMetadataGenerator(self.config, self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_init(self):
        """Test constructor."""
        self.assertEqual(self.generator.metadata_dir, self.test_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "dashboards")))
        self.assertEqual(len(self.generator.dashboard_configs), 2)
    
    def test_generate(self):
        """Test generate method."""
        # Call generate
        count = self.generator.generate()
        
        # Check if dashboard files were created
        sales_file = os.path.join(self.test_dir, "dashboards", "Sales_Dashboard.dashboard-meta.xml")
        marketing_file = os.path.join(self.test_dir, "dashboards", "Marketing_Dashboard.dashboard-meta.xml")
        
        self.assertTrue(os.path.exists(sales_file), "Sales dashboard file was not created")
        self.assertTrue(os.path.exists(marketing_file), "Marketing dashboard file was not created")
        
        # Check if folder file was created
        folder_file = os.path.join(self.test_dir, "dashboards", "My_Dashboards", "Sales_Dashboard.dashboard-meta.xml")
        self.assertTrue(os.path.exists(folder_file), "Dashboard file in folder was not created")
        
        # Check return value
        self.assertEqual(count, 2, "Should create 2 dashboards")
    
    def test_dashboard_xml_content(self):
        """Test generated XML content."""
        # Generate dashboards
        self.generator.generate()
        
        # Check Sales Dashboard content
        sales_file = os.path.join(self.test_dir, "dashboards", "Sales_Dashboard.dashboard-meta.xml")
        with open(sales_file, 'r') as f:
            content = f.read()
            # Check basic dashboard properties
            self.assertIn("<Dashboard", content)
            self.assertIn("<fullName>Sales_Dashboard</fullName>", content)
            self.assertIn("<label>Sales Dashboard</label>", content)
            # Check chart title
            self.assertIn("<title>Revenue by Quarter</title>", content)
            self.assertIn("<report>Sales_Report</report>", content)
    
    def test_component_properties(self):
        """Test component properties in generated XML."""
        # Generate dashboards
        self.generator.generate()
        
        # Check component properties
        marketing_file = os.path.join(self.test_dir, "dashboards", "Marketing_Dashboard.dashboard-meta.xml")
        with open(marketing_file, 'r') as f:
            content = f.read()
            self.assertIn("<componentType>Line</componentType>", content)
            self.assertIn("<title>Campaign Performance</title>", content)
            self.assertIn("<chartAxisRange>Auto</chartAxisRange>", content)
    
    def test_empty_config(self):
        """Test with empty config."""
        # Create generator with empty config
        empty_generator = DashboardMetadataGenerator({"dashboards": {}}, self.test_dir)
        
        # Generate dashboards
        count = empty_generator.generate()
        
        # Check results
        self.assertEqual(count, 0, "No dashboards should be created")
        self.assertEqual(len(os.listdir(os.path.join(self.test_dir, "dashboards"))), 0)


if __name__ == "__main__":
    unittest.main()