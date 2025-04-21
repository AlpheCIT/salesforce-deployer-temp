import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from src.core.authenticator import SalesforceAuthenticator
from src.deployment.deployment import DeploymentManager


class TestAuthenticationFlow(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
        # Create env file
        self.env_file = os.path.join(self.test_dir, ".env")
        with open(self.env_file, 'w') as f:
            f.write("SF_USERNAME=test@example.com\n")
            f.write("SF_PASSWORD=password123\n")
            f.write("SF_SECURITY_TOKEN=token123\n")
            f.write("SF_INSTANCE_URL=https://test.salesforce.com\n")
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    @patch('src.core.authenticator.SalesforceAuthenticator.authenticate')
    @patch('subprocess.run')
    def test_auth_flow_with_deployment(self, mock_run, mock_authenticate):
        """Test authentication flow integrated with deployment."""
        # Mock successful authentication
        mock_authenticate.return_value = True
        SalesforceAuthenticator.access_token = "test_token"
        SalesforceAuthenticator.instance_url = "https://test.salesforce.com"
        
        # Mock successful deployment
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Successfully deployed"
        mock_run.return_value = mock_process
        
        # Create deployment manager
        deploy_dir = os.path.join(self.test_dir, "deploy")
        os.makedirs(os.path.join(deploy_dir, "manifest"), exist_ok=True)
        
        # Create package.xml
        with open(os.path.join(deploy_dir, "manifest", "package.xml"), 'w') as f:
            f.write('<Package xmlns="http://soap.sforce.com/2006/04/metadata"></Package>')
        
        deployment_manager = DeploymentManager(deploy_dir, "56.0")
        
        # Authenticate and deploy
        authenticator = SalesforceAuthenticator()
        auth_result = authenticator.authenticate()
        deploy_result = deployment_manager.deploy()
        
        # Verify results
        self.assertTrue(auth_result)
        self.assertTrue(deploy_result)
        mock_authenticate.assert_called_once()
        self.assertTrue(mock_run.called)
        deploy_calls = [call for call in mock_run.call_args_list if "deploy" in str(call)]
        self.assertTrue(len(deploy_calls) > 0, "No deploy commands were called")


if __name__ == "__main__":
    unittest.main()