import unittest
import os
import tempfile
import shutil

from src.healing.self_healing import SelfHealer


class TestSelfHealing(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.healer = SelfHealer()
        
        # Create some test metadata files with issues
        self.objects_dir = os.path.join(self.test_dir, 'objects')
        os.makedirs(self.objects_dir, exist_ok=True)
        
        # Create object file missing required label
        with open(os.path.join(self.objects_dir, 'Missing_Label__c.object-meta.xml'), 'w') as f:
            f.write("""<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <deploymentStatus>Deployed</deploymentStatus>
    <sharingModel>ReadWrite</sharingModel>
</CustomObject>""")
        
        # Create object file missing nameField
        with open(os.path.join(self.objects_dir, 'Missing_NameField__c.object-meta.xml'), 'w') as f:
            f.write("""<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Test Object</label>
    <deploymentStatus>Deployed</deploymentStatus>
    <sharingModel>ReadWrite</sharingModel>
</CustomObject>""")
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_validate_metadata(self):
        """Test validation of metadata files."""
        issues = self.healer.validate_metadata(self.test_dir)
        
        # Check if issues were detected
        self.assertGreater(len(issues), 0)
        
        # Check for specific issues
        label_issue = False
        name_field_issue = False
        
        for issue in issues:
            if 'Missing_Label' in issue['file'] and 'label' in issue['message']:
                label_issue = True
            elif 'Missing_NameField' in issue['file'] and 'nameField' in issue['message']:
                name_field_issue = True
                
        self.assertTrue(label_issue, "Issue with missing label not detected")
        self.assertTrue(name_field_issue, "Issue with missing nameField not detected")
    
    def test_fix_common_issues(self):
        """Test fixing common issues."""
        # Create a test file with a known issue
        test_file = os.path.join(self.test_dir, "test_object.xml")
        with open(test_file, 'w') as f:
            f.write('<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata"></CustomObject>')
        
        # Call the method
        fixed_issues = self.healer.fix_common_issues(self.test_dir)
        
        # Verify issues were found and fixed
        self.assertGreater(len(fixed_issues), 0, "No issues were fixed")
        self.assertGreater(self.healer.stats["issues_fixed"], 0, "Stats not updated correctly")
    
    def test_analyze_deployment_errors(self):
        """Test analysis of deployment error logs."""
        error_log = """
Error: Invalid field: Account.NonExistentField__c
Error: Required fields are missing: [Name]
Error: CustomObject__c already exists
"""
        analysis = self.healer.analyze_deployment_errors(error_log)
        
        # Check if errors were analyzed
        self.assertEqual(len(analysis), 3)
        
        # Check for specific error types
        error_types = [error['type'] for error in analysis]
        self.assertIn("Invalid field", error_types)
        self.assertIn("Required field missing", error_types)
        self.assertIn("Duplicate name", error_types)


if __name__ == "__main__":
    unittest.main()