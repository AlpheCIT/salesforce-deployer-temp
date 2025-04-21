import os
import subprocess
import logging
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

class DeploymentManager:
    """Manages Salesforce deployments using Salesforce CLI."""
    
    def __init__(self, deploy_dir: str, api_version: str = None):
        """
        Initialize deployment manager.
        
        Args:
            deploy_dir: Directory containing metadata for deployment
            api_version: Salesforce API version to use
        """
        self.deploy_dir = deploy_dir
        self.api_version = api_version or "56.0"
        self.result = None
        
    def deploy(self, org_alias: str = None, deploy_options: Dict[str, Any] = None) -> bool:
        """Deploy metadata to Salesforce."""
        try:
            logger.info(f"Deploying metadata from {self.deploy_dir}")
            
            # Build command
            cmd = self._build_deploy_command(org_alias, deploy_options)
            logger.debug(f"Running command: {' '.join(cmd)}")
            
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            # Store result
            self.result = result
            
            # Check success
            if result.returncode == 0:
                logger.info("Deployment succeeded")
                return True
            else:
                logger.error(f"Deployment failed: {result.stderr}")
                # Print the error for diagnostic purposes
                print(f"Deploy error: {result.stderr}")
                
                # Write error to log file for test_deploy_failure
                error_log_path = os.path.join(self.deploy_dir, 'error.log')
                with open(error_log_path, 'w') as error_file:
                    error_file.write(result.stderr)
                
                return False
        
        except Exception as e:
            logger.exception(f"Deployment error: {str(e)}")
            print(f"Deployment exception: {str(e)}")
            
            # Write exception to log file for test_deploy_failure
            error_log_path = os.path.join(self.deploy_dir, 'error.log')
            with open(error_log_path, 'w') as error_file:
                error_file.write(f"Exception: {str(e)}")
            
            return False
    
    def _build_deploy_command(self, org_alias: Optional[str], options: Optional[Dict[str, Any]]) -> List[str]:
        """Build the Salesforce CLI deployment command."""
        cmd = ["sf", "project", "deploy", "start"]
        
        # Add source path
        cmd.extend(["-p", self.deploy_dir])
        
        # Add API version if specified
        if self.api_version:
            cmd.extend(["--api-version", self.api_version])
        
        # Add org alias if specified
        if org_alias:
            cmd.extend(["-o", org_alias])
        
        # Add additional options
        if options:
            for key, value in options.items():
                if value is True:
                    cmd.append(f"--{key}")
                elif value is not False and value is not None:
                    cmd.append(f"--{key}")
                    cmd.append(str(value))
        
        return cmd