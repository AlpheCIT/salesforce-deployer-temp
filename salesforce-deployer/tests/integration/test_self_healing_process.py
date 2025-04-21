import unittest
import os
import tempfile
import shutil
import json
from unittest.mock import patch, MagicMock

from src.core.deployer import SalesforceDeployer
from src.healing.self_healing import SelfHealer


class TestSelfHealingProcess(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
        # Create sample config file with intentional issues
        self.config_file = os.path.join(self.test_dir, "config.json")
        self.config = {
            "objects": {
                "Problem_Object__c": {
                    # Missing label intentionally
                    "fields": [
                        {"name": "Test_Field__c", "type": "Text"}
                    ]
                }
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)
        
        # Create env file
        self.env_file = os.path.join(self.test_dir, ".env")
        with open(self.env_file, 'w') as f:
            f.write("SF_USERNAME=test@example.com\n")
            f.write("SF_PASSWORD=password123\n")
        
        # Create output dir
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    @patch('src.deployment.deployment.DeploymentManager.deploy')
    @patch('src.healing.self_healing.SelfHealer.validate_metadata')
    @patch('src.healing.self_healing.SelfHealer.fix_common_issues')
    def test_self_healing_process(self, mock_fix_issues, mock_validate, mock_deploy):
        """Test the full self-healing process during deployment."""
        # Mock validation to find issues
        mock_validate.return_value = [
            {
                "file": "Problem_Object__c.object-meta.xml",
                "type": "Required Field Missing",
                "message": "Custom Object is missing required 'label' element",
                "fixable": True
            }
        ]
        
        # Mock fixes applied
        mock_fix_issues.return_value = [
            {
                "file": "Problem_Object__c.object-meta.xml",
                "type": "Required Field Missing",
                "message": "Added missing label element",
                "original_issue": "Custom Object is missing required 'label' element"
            }
        ]
        
        # Mock successful deployment
        mock_deploy.return_value = True
        
        # Create deployer and run with healing
        deployer = SalesforceDeployer(
            config_path=self.config_file,
            output_dir=self.output_dir,
            env_file=self.env_file
        )
        
        # Generate metadata and deploy with healing
        deployer.generate_metadata()
        result = deployer.deploy_with_healing()
        
        # Verify the full process
        self.assertTrue(result)
        mock_validate.assert_called_once()
        mock_fix_issues.assert_called_once()
        mock_deploy.assert_called_once()
    
    def test_self_healing_process(self):
        """Test self-healing process for metadata files."""
        # Create a test file with a known issue
        objects_dir = os.path.join(self.test_dir, "objects")
        os.makedirs(objects_dir, exist_ok=True)
        
        test_file = os.path.join(objects_dir, "Test_Object__c.object-meta.xml")
        with open(test_file, 'w') as f:
            f.write('<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata"></CustomObject>')
        
        # Initialize the self-healer
        healer = SelfHealer(self.test_dir)
        
        # Fix issues
        fixed_issues = healer.fix_common_issues()
        
        # Verify issues were found and fixed
        self.assertTrue(len(fixed_issues) > 0, "No issues were fixed")


if __name__ == "__main__":
    unittest.main()