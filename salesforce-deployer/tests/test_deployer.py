import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from src.core.deployer import SalesforceDeployer


class TestSalesforceDeployer(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create config file
        self.config_file = os.path.join(self.test_dir, "config.json")
        with open(self.config_file, 'w') as f:
            f.write('{"objects": {"Test_Object__c": {"fields": {"Test_Field__c": {"type": "Text"}}}}}')
        
        # Create output directory
        self.output_dir = os.path.join(self.test_dir, "deploy")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create env file - add this
        self.env_file = os.path.join(self.test_dir, ".env")
        with open(self.env_file, 'w') as f:
            f.write("SF_USERNAME=test@example.com\n")
            f.write("SF_PASSWORD=test_password\n")
            f.write("SF_SECURITY_TOKEN=test_token\n")
        
        # Initialize the deployer
        self.deployer = SalesforceDeployer(
            config_path=self.config_file,
            output_dir=self.output_dir
        )
        
        # Initialize mocks
        self.authenticator_mock = MagicMock()
        self.deployment_manager_mock = MagicMock()
        self.self_healer_mock = MagicMock()
        self.metadata_generator_mock = MagicMock()
        
        # Set up authenticator mock to return success by default
        self.authenticator_mock.authenticate.return_value = True
        self.authenticator_mock.access_token = "mock_token"
        self.authenticator_mock.instance_url = "https://test.salesforce.com"
        
        # Replace components with mocks
        self.deployer.authenticator = self.authenticator_mock
        self.deployer.deployment_manager = self.deployment_manager_mock
        self.deployer.self_healer = self.self_healer_mock
        self.deployer.metadata_generator = self.metadata_generator_mock
        
        # Set up stats for tests
        self.deployer.stats = {
            "objects": 1,
            "fields": 1,
            "workflows": 0
        }
            
    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)
    
    @patch('src.config.config_loader.ConfigLoader')
    @patch('src.metadata.generator.MetadataGenerator')
    @patch('src.deployment.deployment.DeploymentManager')
    @patch('src.utils.version_manager.ApiVersionManager')
    @patch('src.healing.self_healing.SelfHealer')
    def test_initialization(self, mock_healer, mock_version_manager, mock_deployment_manager, 
                           mock_metadata_generator, mock_config_loader):
        """Test initialization of SalesforceDeployer."""
        # Setup mocks
        mock_version_manager_instance = mock_version_manager.return_value
        mock_version_manager_instance.get_default_version.return_value = "56.0"
        
        mock_config_loader_instance = mock_config_loader.return_value
        mock_config_loader_instance.load_config.return_value = {"objects": {"Test_Object__c": {}}}
        
        # Initialize the deployer
        deployer = SalesforceDeployer(
            config_path=self.config_file,
            output_dir=self.test_dir,
            env_file=self.env_file
        )
        
        # Check if components were initialized correctly
        self.assertEqual(deployer.deploy_dir, self.test_dir)
        self.assertEqual(deployer.api_version, "56.0")
        
        # Check if methods were called
        mock_config_loader.assert_called_once_with(self.config_file, self.env_file)
        mock_config_loader_instance.load_environment.assert_called_once()
        mock_config_loader_instance.load_config.assert_called_once()
        mock_version_manager.assert_called_once()
        mock_version_manager_instance.get_default_version.assert_called_once()
        mock_metadata_generator.assert_called_once()
        mock_deployment_manager.assert_called_once()
        mock_healer.assert_called_once()
    
    def test_initialization(self):
        """Test deployer initialization."""
        # Create a new deployer with env_file
        deployer = SalesforceDeployer(
            config_path=self.config_file,
            output_dir=self.output_dir,
            env_file=self.env_file
        )
        
        # Verify components are initialized
        self.assertIsNotNone(deployer.metadata_generator)
        self.assertIsNotNone(deployer.deployment_manager)
        self.assertIsNotNone(deployer.authenticator)
        
        # Check initial parameters
        self.assertEqual(deployer.config_path, self.config_file)
        self.assertEqual(deployer.output_dir, self.output_dir)
        self.assertEqual(deployer.env_file, self.env_file)
    
    @patch('src.config.config_loader.ConfigLoader')
    @patch('src.metadata.generator.MetadataGenerator')
    @patch('src.deployment.deployment.DeploymentManager')
    @patch('src.utils.version_manager.ApiVersionManager')
    @patch('src.healing.self_healing.SelfHealer')
    def test_generate_metadata(self, mock_healer, mock_version_manager, mock_deployment_manager, 
                              mock_metadata_generator, mock_config_loader):
        """Test metadata generation."""
        # Setup mocks
        mock_version_manager_instance = mock_version_manager.return_value
        mock_version_manager_instance.get_default_version.return_value = "56.0"
        
        mock_config_loader_instance = mock_config_loader.return_value
        mock_config_loader_instance.load_config.return_value = {"objects": {"Test_Object__c": {}}}
        
        mock_metadata_generator_instance = mock_metadata_generator.return_value
        mock_metadata_generator_instance.get_stats.return_value = {
            "objects_processed": 1,
            "fields_created": 1
        }
        
        # Initialize the deployer
        deployer = SalesforceDeployer(
            config_path=self.config_file,
            output_dir=self.test_dir,
            env_file=self.env_file
        )
        
        # Generate metadata
        deployer.generate_metadata()
        
        # Check if methods were called
        mock_metadata_generator_instance.generate_all.assert_called_once()
        mock_metadata_generator_instance.get_stats.assert_called_once()
        self.assertEqual(deployer.stats, {"objects_processed": 1, "fields_created": 1})
    
    @patch('src.config.config_loader.ConfigLoader')
    @patch('src.metadata.generator.MetadataGenerator')
    @patch('src.deployment.deployment.DeploymentManager')
    @patch('src.utils.version_manager.ApiVersionManager')
    @patch('src.healing.self_healing.SelfHealer')
    def test_deploy_metadata(self, mock_healer, mock_version_manager, mock_deployment_manager, 
                            mock_metadata_generator, mock_config_loader):
        """Test metadata deployment."""
        # Setup mocks
        mock_version_manager_instance = mock_version_manager.return_value
        mock_version_manager_instance.get_default_version.return_value = "56.0"
        
        mock_config_loader_instance = mock_config_loader.return_value
        mock_config_loader_instance.load_config.return_value = {"objects": {"Test_Object__c": {}}}
        
        mock_deployment_manager_instance = mock_deployment_manager.return_value
        mock_deployment_manager_instance.deploy.return_value = True
        
        # Initialize the deployer
        deployer = SalesforceDeployer(
            config_path=self.config_file,
            output_dir=self.test_dir,
            env_file=self.env_file
        )
        
        # Deploy metadata
        result = deployer.deploy_metadata()
        
        # Check if methods were called and result is correct
        mock_deployment_manager_instance.deploy.assert_called_once()
        self.assertTrue(result)
    
    @patch('src.config.config_loader.ConfigLoader')
    @patch('src.metadata.generator.MetadataGenerator')
    @patch('src.deployment.deployment.DeploymentManager')
    @patch('src.utils.version_manager.ApiVersionManager')
    @patch('src.healing.self_healing.SelfHealer')
    def test_deploy_with_healing(self, mock_healer, mock_version_manager, mock_deployment_manager, 
                                mock_metadata_generator, mock_config_loader):
        """Test deployment with self-healing capabilities."""
        # Setup mocks
        mock_version_manager_instance = mock_version_manager.return_value
        mock_version_manager_instance.get_default_version.return_value = "56.0"
        
        mock_config_loader_instance = mock_config_loader.return_value
        mock_config_loader_instance.load_config.return_value = {"objects": {"Test_Object__c": {}}}
        
        mock_metadata_generator_instance = mock_metadata_generator.return_value
        mock_metadata_generator_instance.get_metadata_dir.return_value = os.path.join(self.test_dir, "metadata")
        
        mock_deployment_manager_instance = mock_deployment_manager.return_value
        mock_deployment_manager_instance.deploy.return_value = True
        
        mock_healer_instance = mock_healer.return_value
        mock_healer_instance.validate_metadata.return_value = []
        mock_healer_instance.optimize_deployment_order.return_value = {"1-Objects": ["Test_Object__c"]}
        
        # Initialize the deployer
        deployer = SalesforceDeployer(
            config_path=self.config_file,
            output_dir=self.test_dir,
            env_file=self.env_file
        )
        
        # Deploy with healing
        result = deployer.deploy_with_healing()
        
        # Check if methods were called and result is correct
        mock_healer_instance.validate_metadata.assert_called_once()
        mock_healer_instance.optimize_deployment_order.assert_called_once()
        mock_deployment_manager_instance.deploy.assert_called_once()
        self.assertTrue(result)
    
    def test_deploy_metadata(self):
        """Test deploying metadata."""
        # Set up mock for deploy method
        with patch.object(self.deployer.deployment_manager, 'deploy') as mock_deploy:
            mock_deploy.return_value = True
            
            # Call deploy_metadata
            result = self.deployer.deploy_metadata()
            
            # Check if deploy was called
            self.assertTrue(result)
            mock_deploy.assert_called_once()
    
    def test_deploy_with_healing(self):
        """Test deploying with self-healing."""
        # Create mock for self_healer and deployment_manager
        with patch.object(self.deployer.self_healer, 'fix_common_issues') as mock_fix_issues, \
             patch.object(self.deployer.deployment_manager, 'deploy') as mock_deploy:
            
            # Set return values
            mock_fix_issues.return_value = [{"file": "test.xml", "message": "Fixed issue"}]
            mock_deploy.return_value = True
            
            # Call deploy with healing
            result = self.deployer.deploy_with_healing()
            
            # Verify calls and result
            self.assertTrue(result)
            mock_fix_issues.assert_called_once()
            mock_deploy.assert_called_once()


if __name__ == "__main__":
    unittest.main()