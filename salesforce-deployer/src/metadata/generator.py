import os
import logging
from typing import Dict, Any
import xml.etree.ElementTree as ET

from src.metadata.objects import ObjectMetadataGenerator
from src.metadata.workflows import WorkflowMetadataGenerator
from src.metadata.dashboards import DashboardMetadataGenerator
from src.metadata.flows import FlowMetadataGenerator
from src.metadata.package import PackageGenerator

logger = logging.getLogger(__name__)

class MetadataGenerator:
    """Coordinates generation of all Salesforce metadata files."""
    
    def __init__(self, config, output_dir, api_version):
        """Initialize metadata generator."""
        self.config = config
        self.output_dir = output_dir
        self.deploy_dir = output_dir  # Add this line for backward compatibility
        self.api_version = api_version
        
        # Create SFDX project structure
        self.metadata_dir = os.path.join(output_dir, "force-app", "main", "default")
        os.makedirs(self.metadata_dir, exist_ok=True)
        
        # Initialize component generators
        self.object_generator = ObjectMetadataGenerator(config, self.metadata_dir)
        self.workflow_generator = WorkflowMetadataGenerator(config, self.metadata_dir)
        self.dashboard_generator = DashboardMetadataGenerator(config, self.metadata_dir)
        self.flow_generator = FlowMetadataGenerator(config, self.metadata_dir)
        self.package_generator = PackageGenerator(config, output_dir, api_version)
        
        # Initialize stats
        self.stats = {}
    
    def generate_all(self):
        """Generate all metadata from configurations."""
        # Reset stats before generation
        self.stats = {
            "objects_processed": 0,
            "fields_created": 0,
            "workflow_rules_created": 0,
            "dashboards_created": 0,
            "flows_created": 0,
            "errors": 0,
            # Simplified stats for tests
            "objects": 0,
            "fields": 0,
            "workflows": 0
        }
        
        # Generate all types of metadata
        self._generate_objects()
        self._generate_workflows()
        self._generate_dashboards()
        self._generate_flows()
        self._generate_package()
        
        return self.stats
    
    def _generate_objects(self):
        """Generate object metadata files."""
        objects_created = self.object_generator.generate()
        
        # Update stats
        self.stats["objects_processed"] = objects_created
        self.stats["fields_created"] = self.object_generator.stats.get("fields_created", 0)
        self.stats["objects"] = objects_created  # For test compatibility
        self.stats["fields"] = self.stats["fields_created"]  # For test compatibility

    def _generate_workflows(self):
        """Generate workflow metadata files."""
        workflows_created = self.workflow_generator.generate()
        
        # Update stats
        self.stats["workflow_rules_created"] = self.workflow_generator.stats.get("rules_created", 0)
        self.stats["workflows"] = workflows_created  # For test compatibility

    def _generate_dashboards(self):
        """Generate dashboard metadata files."""
        dashboards_created = self.dashboard_generator.generate()
        
        # Update stats
        self.stats["dashboards_created"] = dashboards_created

    def _generate_flows(self):
        """Generate flow metadata files."""
        flows_created = self.flow_generator.generate()
        
        # Update stats
        self.stats["flows_created"] = flows_created
    
    def _generate_package(self):
        """Generate package.xml manifest file."""
        logger.info("Generating package.xml manifest...")
        
        # Use the package_generator that's already initialized
        self.package_generator.generate()
    
    def get_stats(self) -> Dict[str, int]:
        """Get metadata generation statistics."""
        return self.stats
    
    def get_metadata_dir(self) -> str:
        """Get the metadata directory path."""
        return self.metadata_dir