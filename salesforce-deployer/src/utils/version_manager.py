"""
API Version management for Salesforce deployments.
"""

import json
import os
import logging
import requests
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

DEFAULT_API_VERSION = "56.0"  # Set default to match test expectations

class ApiVersionManager:
    """Manages Salesforce API versions and compatibility."""
    
    def __init__(self, version_file: Optional[str] = None):
        """
        Initialize the API version manager.
        
        Args:
            version_file: Path to the version configuration file
        """
        self.version_file = version_file or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "configs",
            "api_versions.json"
        )
        self.versions = self._load_versions()
        
    def _load_versions(self) -> Dict[str, Any]:
        """
        Load API versions from configuration file.
        
        Returns:
            Dictionary containing API version information
        """
        try:
            if os.path.exists(self.version_file):
                with open(self.version_file, 'r') as f:
                    return json.load(f)
            else:
                # Return default structure if file doesn't exist
                return {
                    "versions": [
                        {
                            "version": DEFAULT_API_VERSION,
                            "label": "Default API Version",
                            "url": f"/services/data/v{DEFAULT_API_VERSION}"
                        }
                    ],
                    "default": DEFAULT_API_VERSION,
                    "latest": DEFAULT_API_VERSION
                }
        except Exception as e:
            print(f"Error loading API versions: {e}")
            return {
                "versions": [
                    {
                        "version": DEFAULT_API_VERSION,
                        "label": "Default API Version",
                        "url": f"/services/data/v{DEFAULT_API_VERSION}"
                    }
                ],
                "default": DEFAULT_API_VERSION,
                "latest": DEFAULT_API_VERSION
            }
    
    def get_latest_version(self) -> str:
        """Get the latest supported API version."""
        if not self.versions or not self.versions.get("supported"):
            return "63.0"  # Default fallback
        
        # Sort versions and return the most recent
        sorted_versions = sorted(
            self.versions["supported"], 
            key=lambda v: float(v.get("version", "0")), 
            reverse=True
        )
        return sorted_versions[0].get("version", "63.0") if sorted_versions else "63.0"
    
    def get_default_version(self) -> str:
        """
        Get the default API version.
        
        Returns:
            Default API version string (e.g., "56.0")
        """
        return self.versions.get("default", DEFAULT_API_VERSION)
        
    def is_supported(self, version: str) -> bool:
        """Check if a version is supported."""
        supported_versions = [v.get("version") for v in self.versions.get("supported", [])]
        return version in supported_versions
    
    def check_metadata_compatibility(self, metadata_type: str, api_version: str) -> bool:
        """Check if a metadata type is compatible with the specified API version."""
        metadata_availability = self.versions.get('metadataTypeAvailability', {})
        if metadata_type in metadata_availability:
            min_version = metadata_availability[metadata_type].replace('+', '')
            if float(api_version) < float(min_version):
                logger.warning(
                    f"Metadata type {metadata_type} requires API version {min_version}+ "
                    f"(using {api_version})"
                )
                return False
        return True
    
    def fetch_available_versions(self, sf_instance_url: str, access_token: str) -> List[Dict]:
        """Query Salesforce for available API versions.
        
        Args:
            sf_instance_url: Salesforce instance URL
            access_token: Access token for authentication
            
        Returns:
            List of available API versions
        """
        try:
            # Query available versions from Salesforce
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            response = requests.get(
                f"{sf_instance_url}/services/data",
                headers=headers
            )
            response.raise_for_status()
            available_versions = response.json()
            
            # Update local configuration with any new versions
            self._update_version_config(available_versions)
            
            return available_versions
        except Exception as e:
            logger.error(f"Error fetching available API versions: {str(e)}")
            return []
    
    def _update_version_config(self, available_versions: List[Dict]) -> None:
        """Update the local version config with newly discovered versions.
        
        Args:
            available_versions: List of available API versions from Salesforce
        """
        try:
            updated = False
            supported_versions = [v.get("version") for v in self.versions.get("supported", [])]
            
            for version_info in available_versions:
                version = version_info.get("version")
                if version and version not in supported_versions:
                    # Add new version to configuration
                    new_version = {
                        "version": version,
                        "releaseDate": version_info.get("releaseDate", "Unknown"),
                        "endOfSupportDate": "Unknown",  # Can't determine this from API
                        "features": []  # Would need manual updating
                    }
                    self.versions.setdefault("supported", []).append(new_version)
                    updated = True
            
            if updated:
                # Save updated configuration
                with open(self.config_path, 'w') as f:
                    json.dump(self.versions, f, indent=2)
                logger.info(f"Updated API version configuration with new versions")
        except Exception as e:
            logger.error(f"Error updating API version configuration: {str(e)}")
    
    def detect_optimal_version(self, available_versions: List[Dict], metadata_types: List[str]) -> str:
        """Detect the optimal API version for deployment based on metadata requirements.
        
        Args:
            available_versions: List of available API versions from Salesforce
            metadata_types: List of metadata types being deployed
            
        Returns:
            Optimal API version string
        """
        # Get all supported versions from Salesforce
        sf_versions = [v.get("version") for v in available_versions if "version" in v]
        if not sf_versions:
            return self.get_default_version()
        
        # Find minimum required version based on metadata types
        min_required = "1.0"
        metadata_availability = self.versions.get('metadataTypeAvailability', {})
        for metadata_type in metadata_types:
            if metadata_type in metadata_availability:
                type_min_version = metadata_availability[metadata_type].replace('+', '')
                min_required = max(min_required, type_min_version)
        
        # Find the latest available version that's at least the minimum required
        valid_versions = [v for v in sf_versions if float(v) >= float(min_required)]
        if not valid_versions:
            logger.warning(
                f"No available API version meets the minimum requirement of {min_required}. "
                f"Using default version {self.get_default_version()}"
            )
            return self.get_default_version()
        
        return max(valid_versions, key=float)