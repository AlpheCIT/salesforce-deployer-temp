import unittest
import os
import tempfile
import shutil
import json
from unittest.mock import patch

from src.core.deployer import SalesforceDeployer


class TestEndToEndDeployment(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create test config
        self.config_file = os.path.join(self.test_dir, "config.json")  # Renamed from config_path
        with open(self.config_file, 'w') as f:
            f.write('{"objects": {"Test_Object__c": {"fields": {"Test_Field__c": {"type": "Text"}}}}}')
        
        # Create output directory
        self.output_dir = os.path.join(self.test_dir, "deploy")
        os.makedirs(os.path.join(self.output_dir, "manifest"), exist_ok=True)
        
        # Create env file
        self.env_file = os.path.join(self.test_dir, ".env")
        with open(self.env_file, 'w') as f:
            f.write("SF_USERNAME=test@example.com\n")
            f.write("SF_PASSWORD=test_password\n")
            f.write("SF_SECURITY_TOKEN=test_token\n")
        
        # Create package.xml
        with open(os.path.join(self.output_dir, "manifest", "package.xml"), 'w') as f:
            f.write('<Package xmlns="http://soap.sforce.com/2006/04/metadata"><version>56.0</version></Package>')
            
    def tearDown(self):
        # Clean up temporary files
        shutil.rmtree(self.test_dir)
    
    def test_end_to_end_deployment(self):
        """Test end-to-end deployment process."""
        # We need to mock several components for the test
        with patch('src.core.authenticator.SalesforceAuthenticator.authenticate', return_value=True), \
             patch('src.deployment.deployment.DeploymentManager.deploy', return_value=True), \
             patch('src.metadata.generator.MetadataGenerator.generate_all', return_value=True), \
             patch('src.metadata.generator.MetadataGenerator.get_stats', return_value={"objects": 1, "fields": 2}):
            
            # Initialize deployer
            deployer = SalesforceDeployer(
                config_path=self.config_file,
                output_dir=self.output_dir,
                env_file=self.env_file
            )
            
            # Generate metadata
            generate_result = deployer.generate_metadata()
            
            # Deploy metadata
            deploy_result = deployer.deploy_metadata()
            
            # Verify both operations were successful
            self.assertTrue(generate_result, "Metadata generation failed")
            self.assertTrue(deploy_result, "Metadata deployment failed")

    @patch('src.core.authenticator.SalesforceAuthenticator.authenticate', return_value=True)
    @patch('src.deployment.deployment.DeploymentManager.deploy', return_value=True)
    def test_self_healing_deployment(self, mock_deploy, mock_auth):
        """Test deployment with self-healing capabilities."""
        # Create a deployer with self-healing
        deployer = SalesforceDeployer(
            config_path=self.config_file,
            output_dir=self.output_dir,
            env_file=self.env_file
        )
        
        # Mock the self_healer.fix_common_issues method
        with patch.object(deployer.self_healer, 'fix_common_issues') as mock_fix_issues:
            # Set return value for fix_common_issues
            mock_fix_issues.return_value = [{"file": "test.xml", "fixed": True}]
            
            # Call deploy_with_healing
            result = deployer.deploy_with_healing()
            
            # Verify results
            self.assertTrue(result, "Deployment with healing failed")
            mock_fix_issues.assert_called_once()
            mock_deploy.assert_called_once()


if __name__ == "__main__":
    unittest.main()