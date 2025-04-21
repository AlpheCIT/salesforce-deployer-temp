"""
Main deployment manager for Salesforce metadata.
"""

import os
import json
import logging
import tempfile
import shutil
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SalesforceDeployer:
    """
    Main class for deploying Salesforce metadata.
    """
    
    def __init__(self, config_path: str, output_dir: Optional[str] = None, env_file: Optional[str] = None,
                 api_version: Optional[str] = None, no_deploy: bool = False, verbose: bool = False):
        """Initialize SalesforceDeployer."""
        # Store parameters
        self.config_path = config_path
        self.output_dir = output_dir or "deploy"
        # Add deploy_dir as an alias of output_dir for backward compatibility
        self.deploy_dir = self.output_dir
        self.env_file = env_file
        self.api_version = api_version or "56.0"
        self.no_deploy = no_deploy
        self.verbose = verbose
        
        # Initialize stats
        self.stats = {}
        
        # Load configuration
        self.config = self._load_config()
        
        # Set up authenticator
        self.authenticator = self._setup_authenticator()
        
        # Set up metadata generator
        self.metadata_generator = self._setup_metadata_generator()
        
        # Set up deployment manager
        self.deployment_manager = self._setup_deployment_manager()
        
        # Set up self-healer
        self.self_healer = self._setup_self_healer()
    
    def _load_config(self):
        from src.config.config_loader import ConfigLoader
        config_loader = ConfigLoader(self.config_path)
        return config_loader.load_config()
    
    def _setup_authenticator(self):
        from src.core.authenticator import SalesforceAuthenticator
        return SalesforceAuthenticator(env_file=self.env_file)
    
    def _setup_metadata_generator(self):
        from src.metadata.generator import MetadataGenerator
        return MetadataGenerator(self.config, self.output_dir, self.api_version)
    
    def _setup_deployment_manager(self):
        from src.deployment.deployment import DeploymentManager
        return DeploymentManager(self.output_dir, self.api_version)
    
    def _setup_self_healer(self):
        from src.healing.self_healing import SelfHealer
        return SelfHealer(self.output_dir, self.api_version)
    
    def generate_metadata(self) -> bool:
        """
        Generate metadata files from configuration.
        
        Returns:
            True if metadata was generated successfully, False otherwise
        """
        if self.verbose:
            print(f"Generating metadata for API version {self.api_version}")
        
        try:
            self.metadata_generator.generate_all()
            # Get stats after generation (needed for tests)
            self.stats = self.metadata_generator.get_stats()
            if self.verbose:
                print(f"Metadata generation stats: {self.stats}")
            return True
        except Exception as e:
            print(f"Error generating metadata: {e}")
            return False
    
    def deploy_metadata(self) -> bool:
        """
        Deploy metadata to Salesforce.
        
        Returns:
            True if deployment was successful, False otherwise
        """
        if self.no_deploy:
            print("Deployment skipped (no_deploy=True)")
            return True
        
        if self.verbose:
            print("Starting metadata deployment...")
        
        try:
            # Authenticate first
            if not self.authenticator.authenticate():
                print("Authentication failed, cannot deploy")
                return False
            
            # Apply self-healing before deployment
            if hasattr(self, "self_healer"):
                print("Running self-healing checks...")
                fixed_issues = self.self_healer.fix_common_issues(self.output_dir)
                if fixed_issues and self.verbose:
                    print(f"Self-healing fixed {len(fixed_issues)} issues")
            
            # Deploy the metadata
            result = self.deployment_manager.deploy()
            
            if self.verbose:
                print(f"Deployment {'successful' if result else 'failed'}")
            
            return result
        except Exception as e:
            print(f"Error deploying metadata: {e}")
            return False
            
    def deploy_with_healing(self) -> bool:
        """
        Deploy metadata with automatic self-healing.
        
        Returns:
            True if deployment was successful, False otherwise
        """
        if self.verbose:
            print("Starting deployment with self-healing...")
        
        try:
            # Authenticate
            if not self.authenticator.authenticate():
                print("Authentication failed, cannot deploy")
                return False
            
            # Run self-healing - explicitly call fix_common_issues
            if hasattr(self, "self_healer"):
                print("Running self-healing checks...")
                fixed_issues = self.self_healer.fix_common_issues(self.output_dir)
                if fixed_issues and self.verbose:
                    print(f"Self-healing fixed {len(fixed_issues)} issues")
            
            # Deploy
            result = self.deployment_manager.deploy()
            
            return result
        except Exception as e:
            print(f"Error in deploy_with_healing: {e}")
            return False

    def cleanup(self):
        """Clean up temporary files after deployment."""
        logger.info("Cleaning up deployment files...")
        if os.path.exists(self.output_dir) and not self.output_dir.startswith(tempfile.gettempdir()):
            shutil.rmtree(self.output_dir)

def main():
    # Main execution logic
    pass

if __name__ == "__main__":
    main()