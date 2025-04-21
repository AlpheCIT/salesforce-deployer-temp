import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Handles loading and validating configuration for Salesforce deployments."""
    
    def __init__(self, config_path: str, env_file: str = '.env'):
        """
        Initialize the config loader.
        
        Args:
            config_path: Path to the JSON configuration file
            env_file: Path to the environment file with Salesforce credentials
        """
        self.config_path = config_path
        self.env_file = env_file
        
    def load_environment(self):
        """Load environment variables from .env file."""
        # Load environment variables
        if not os.path.exists(self.env_file):
            logger.error(f"Environment file not found: {self.env_file}")
            raise FileNotFoundError(f"Environment file not found: {self.env_file}")
            
        load_dotenv(self.env_file)
        self._validate_environment_variables()
    
    def _validate_environment_variables(self):
        """Validate that required environment variables are set."""
        required_vars = ['SF_USERNAME', 'SF_PASSWORD']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def load_config(self) -> Dict[str, Any]:
        """Load and validate the configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
            
            # Validate configuration structure
            self._validate_config(config)
            
            return config
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {str(e)}")
            raise ValueError(f"Invalid JSON in configuration file: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise
    
    def _validate_config(self, config: Dict[str, Any]):
        """Validate the configuration structure."""
        if not isinstance(config, dict):
            raise ValueError("Configuration root must be a JSON object")
        
        # Validate required sections exist
        required_sections = []  # Add required sections as needed
        
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required section '{section}' in configuration")