import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock

from src.deployment.deployment import DeploymentManager


class TestDeployment(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create a manifest directory and package.xml
        manifest_dir = os.path.join(self.test_dir, "manifest")
        os.makedirs(manifest_dir, exist_ok=True)
        
        # Create package.xml
        package_xml = os.path.join(manifest_dir, "package.xml")
        with open(package_xml, 'w') as f:
            f.write('<Package xmlns="http://soap.sforce.com/2006/04/metadata"><version>56.0</version></Package>')
        
        # Initialize deployment manager
        self.deployment_manager = DeploymentManager(self.test_dir, "56.0")
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_deploy_success(self):
        """Test successful deployment."""
        # Mock subprocess.run
        with patch('subprocess.run') as mock_run:
            # Set up mock response
            mock_process = MagicMock()
            mock_process.returncode = 0
            mock_process.stdout = "Deployment succeeded"
            mock_run.return_value = mock_process
            
            # Call deploy
            result = self.deployment_manager.deploy()
            
            # Check results
            self.assertTrue(result)
            # Check that subprocess.run was called
            self.assertTrue(mock_run.called)
            # Extract calls that contain "deploy"
            deploy_calls = [call for call in mock_run.call_args_list 
                            if any("deploy" in str(arg) for arg in call[0][0])]
            # Verify at least one deploy call was made
            self.assertTrue(len(deploy_calls) > 0)
        
    def test_deploy_failure(self):
        """Test failed deployment."""
        with patch('subprocess.run') as mock_run:
            # Set up mock return value
            mock_result = MagicMock()
            mock_result.returncode = 1  # non-zero indicates failure
            mock_result.stdout = "Some output"
            mock_result.stderr = "Error: deployment failed"
            mock_run.return_value = mock_result
            
            # Call the method
            result = self.deployment_manager.deploy()
            
            # Assert result is False (indicating failure)
            self.assertFalse(result)
            
            # Assert subprocess.run was called
            mock_run.assert_called()
        
    @patch('subprocess.run')
    def test_deploy_failure(self, mock_run):
        """Test failed deployment using Salesforce CLI."""
        # Setup mock response
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = "Deployment failed"
        mock_process.stderr = "Error: Invalid field"
        mock_run.return_value = mock_process
        
        # Run deployment
        result = self.deployment_manager.deploy()
        
        # Verify deployment
        self.assertFalse(result)
        self.assertTrue(mock_run.called)
        deploy_calls = [call for call in mock_run.call_args_list if "deploy" in str(call)]
        self.assertTrue(len(deploy_calls) > 0, "No deploy commands were called")
        
        # Check if error log was created
        error_log_path = os.path.join(self.test_dir, 'error.log')
        self.assertTrue(os.path.exists(error_log_path))
        with open(error_log_path, 'r') as f:
            content = f.read()
            self.assertIn("Error: Invalid field", content)


if __name__ == "__main__":
    unittest.main()