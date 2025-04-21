import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from src.core.deployer import SalesforceDeployer


class TestDeployer(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, 'config.json')
        self.env_file = os.path.join(self.test_dir, '.env')
        self.output_dir = os.path.join(self.test_dir, 'output')
        
        # Create dummy files
        with open(self.config_file, 'w') as f:
            f.write('{"objects": {"Test_Object__c": {"label": "Test Object"}}}')
        
        with open(self.env_file, 'w') as f:
            f.write("SF_USERNAME=test@example.com\nSF_PASSWORD=password123")
            
        os.makedirs(self.output_dir, exist_ok=True)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
    
    @patch('src.config.config_loader.ConfigLoader')
    @patch('src.metadata.generator.MetadataGenerator')
    @patch('src.deployment.deployment.DeploymentManager')
    @patch('src.utils.version_manager.ApiVersionManager')
    def test_initialization(self, mock_version_manager, mock_deployment_manager, 
                           mock_metadata_generator, mock_config_loader):
        """Test the initialization of the deployer."""
        # Setup mocks
        mock_version_manager.return_value.get_default_version.return_value = "56.0"
        mock_config_loader.return_value.load_config.return_value = {"objects": {}}
        
        # Initialize deployer
        deployer = SalesforceDeployer(
            config_path=self.config_file,
            output_dir=self.output_dir,
            env_file=self.env_file
        )
        
        # Verify initialization
        self.assertEqual(deployer.deploy_dir, self.output_dir)
        self.assertEqual(deployer.api_version, "56.0")
        mock_config_loader.assert_called_once()
        mock_metadata_generator.assert_called_once()
        mock_deployment_manager.assert_called_once()
        
    @patch('src.config.config_loader.ConfigLoader')
    @patch('src.metadata.generator.MetadataGenerator')
    @patch('src.deployment.deployment.DeploymentManager')
    @patch('src.utils.version_manager.ApiVersionManager')
    def test_generate_metadata(self, mock_version_manager, mock_deployment_manager, 
                              mock_metadata_generator, mock_config_loader):
        """Test metadata generation process."""
        # Setup mocks
        mock_version_manager.return_value.get_default_version.return_value = "56.0"
        mock_config_loader.return_value.load_config.return_value = {"objects": {}}
        mock_metadata_generator.return_value.get_stats.return_value = {
            "objects_processed": 1,
            "fields_created": 2
        }
        
        # Initialize deployer
        deployer = SalesforceDeployer(
            config_path=self.config_file,
            output_dir=self.output_dir,
            env_file=self.env_file
        )
        
        # Generate metadata
        deployer.generate_metadata()
        
        # Verify generation
        mock_metadata_generator.return_value.generate_all.assert_called_once()
        mock_metadata_generator.return_value.get_stats.assert_called_once()
        self.assertEqual(deployer.stats, {"objects_processed": 1, "fields_created": 2})


if __name__ == "__main__":
    unittest.main()