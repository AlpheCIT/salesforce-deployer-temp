#!/usr/bin/env python3
"""
Salesforce Schema Deployment Tool

This script deploys Salesforce configuration from a JSON schema file using the Metadata API.
It handles objects, fields, workflow rules, dashboards, and other configurations.

Features:
- Uses Salesforce Metadata API through CLI for deployment
- Supports all object types and field types in the provided JSON structure
- Validates JSON structure before deployment
- Provides detailed logging and error handling
- Supports deployment to any Salesforce org with proper authentication

Usage:
    python sf_deploy.py --config CONFIG_FILE [--env ENV_FILE] [--output OUTPUT_DIR]

Arguments:
    --config        Path to the JSON configuration file (default: config.json)
    --env           Path to the .env file with credentials (default: .env)
    --output        Path to store temporary deployment files (default: temp_deploy)
    --verbose       Enable verbose logging
    --no-deploy     Generate metadata files without deploying
    --validate      Validate the JSON structure without deployment

Example:
    python sf_deploy.py --config qualys_schema.json --env prod.env
"""

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Add required dependencies
try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required package 'python-dotenv' not found.")
    print("Please install it using: pip install python-dotenv")
    sys.exit(1)

# Set up logging with timestamp format
log_format = '%(asctime)s - %(levelname)s - %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'salesforce_deploy_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

class SalesforceDeployer:
    """Primary class for deploying Salesforce metadata from JSON configuration."""
    
    def __init__(self, config_path: str, output_dir: str = None, env_file: str = '.env'):
        """
        Initialize the deployer with configuration.
        
        Args:
            config_path: Path to the JSON configuration file
            output_dir: Directory to store deployment files (temp directory if None)
            env_file: Path to the environment file with Salesforce credentials
        """
        self.start_time = datetime.now()
        
        # Load environment variables
        if not os.path.exists(env_file):
            logger.error(f"Environment file not found: {env_file}")
            raise FileNotFoundError(f"Environment file not found: {env_file}")
        load_dotenv(env_file)
        
        # Check for required environment variables
        self._validate_environment_variables()
        
        # Store configuration path
        self.config_path = config_path
        
        # Create deployment directory
        if output_dir:
            self.deploy_dir = output_dir
            os.makedirs(self.deploy_dir, exist_ok=True)
        else:
            self.deploy_dir = tempfile.mkdtemp()
        
        logger.info(f"Deployment directory: {self.deploy_dir}")
        
        # Load and validate configuration
        self.config = self._load_and_validate_config()
        
        # Create metadata directory structure
        self.metadata_dir = os.path.join(self.deploy_dir, 'force-app', 'main', 'default')
        self.objects_dir = os.path.join(self.metadata_dir, 'objects')
        self.workflows_dir = os.path.join(self.metadata_dir, 'workflows')
        self.dashboards_dir = os.path.join(self.metadata_dir, 'dashboards')
        
        # Create directory structure
        for directory in [self.objects_dir, self.workflows_dir, self.dashboards_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Create sfdx project files
        self._create_sfdx_project_files()
        
        # Statistics for reporting
        self.stats = {
            "objects_processed": 0,
            "fields_created": 0,
            "workflow_rules_created": 0,
            "dashboards_created": 0,
            "errors": 0
        }

    def _validate_environment_variables(self):
        """Check if required environment variables are set."""
        required_vars = ['SF_USERNAME', 'SF_PASSWORD']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            logger.error("Please check your .env file")
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Check for instance URL
        if not (os.getenv('SF_INSTANCE_URL') or os.getenv('SF_LOGIN_URL')):
            logger.error("Missing SF_INSTANCE_URL or SF_LOGIN_URL environment variable")
            raise ValueError("Missing SF_INSTANCE_URL or SF_LOGIN_URL environment variable")

    def _load_and_validate_config(self) -> Dict[str, Any]:
        """Load and validate the configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            logger.info(f"Configuration loaded from {self.config_path}")
            
            # Validate configuration structure
            if not isinstance(config, dict):
                raise ValueError("Configuration root must be a JSON object")
            
            # Check for required sections
            required_sections = ['objects']
            missing_sections = [section for section in required_sections if section not in config]
            
            if missing_sections:
                logger.warning(f"Missing recommended sections in configuration: {', '.join(missing_sections)}")
            
            # Log statistics about the configuration
            object_count = len(config.get('objects', {}))
            field_count = sum(len(obj_config.get('fields', [])) for obj_config in config.get('objects', {}).values())
            workflow_count = len(config.get('workflowRules', {}))
            dashboard_count = len(config.get('dashboards', {}))
            
            logger.info(f"Configuration contains: {object_count} objects, {field_count} fields, " 
                       f"{workflow_count} workflow rules, {dashboard_count} dashboards")
            
            return config
        
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {str(e)}")
            raise ValueError(f"Invalid JSON in configuration file: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise

    def _create_sfdx_project_files(self):
        """Create the project configuration files for a valid Salesforce DX project."""
        # Create sfdx-project.json
        project_config = {
            "packageDirectories": [
                {
                    "path": "force-app",
                    "default": True,
                    "package": "SFDeploy",
                    "versionName": "Version 1.0",
                    "versionNumber": "1.0.0.NEXT"
                }
            ],
            "namespace": "",
            "sfdcLoginUrl": os.getenv('SF_INSTANCE_URL') or os.getenv('SF_LOGIN_URL') or "https://login.salesforce.com",
            "sourceApiVersion": "63.0"
        }
        
        project_file = os.path.join(self.deploy_dir, 'sfdx-project.json')
        with open(project_file, 'w') as f:
            json.dump(project_config, f, indent=4)
        
        # Create .forceignore file
        forceignore_content = """# Ignore profiles
**/profiles/**

# Standard ignore patterns
**/.eslintrc.json
**/.DS_Store
**/.sfdx
**/.vscode
**/jsconfig.json
**/.idea
"""
        
        forceignore_file = os.path.join(self.deploy_dir, '.forceignore')
        with open(forceignore_file, 'w') as f:
            f.write(forceignore_content)
        
        logger.debug("Created SFDX project configuration files")

    def generate_metadata(self):
        """Generate metadata files for all components in the configuration."""
        logger.info("Starting metadata generation...")
        
        # Process objects and fields
        self._generate_object_metadata()
        
        # Process workflow rules
        self._generate_workflow_metadata()
        
        # Process dashboards
        self._generate_dashboard_metadata()
        
        # Process other components from the rich JSON structure
        self._generate_lightningflow_metadata()
        self._generate_service_console_metadata()
        
        # Create package.xml
        self._create_package_xml()
        
        logger.info(f"Metadata generation completed. Statistics: "
                   f"{self.stats['objects_processed']} objects, "
                   f"{self.stats['fields_created']} fields, "
                   f"{self.stats['workflow_rules_created']} workflow rules, "
                   f"{self.stats['dashboards_created']} dashboards")

    def _generate_object_metadata(self):
        """Generate metadata for objects and their fields."""
        objects = self.config.get('objects', {})
        
        for obj_name, obj_config in objects.items():
            logger.info(f"Processing object: {obj_name}")
            
            # Determine if this is a custom object or standard object
            is_custom_object = obj_name.endswith('__c')
            
            # For custom objects, create the object metadata
            if is_custom_object:
                self._generate_custom_object_metadata(obj_name, obj_config)
            
            # Create object directory
            obj_dir = os.path.join(self.objects_dir, obj_name)
            os.makedirs(obj_dir, exist_ok=True)
            
            # Create fields directory
            fields_dir = os.path.join(obj_dir, 'fields')
            os.makedirs(fields_dir, exist_ok=True)
            
            # Process fields
            for field in obj_config.get('fields', []):
                try:
                    field_name = field.get('name')
                    field_type = field.get('type')
                    field_values = field.get('values', [])
                    reference_to = field.get('referenceTo')
                    formula = field.get('formula')
                    formula_return_type = field.get('formulaReturnType')
                    
                    # Skip fields without name or type
                    if not field_name or not field_type:
                        logger.warning(f"Skipping field with missing name or type: {field}")
                        continue
                    
                    logger.info(f"Generating metadata for field {field_name} of type {field_type}")
                    
                    # Generate field XML with all parameters
                    field_xml = self._generate_field_xml(
                        field_name, 
                        field_type, 
                        field_values, 
                        reference_to,
                        formula,
                        formula_return_type
                    )
                    
                    # Write to file
                    field_file = os.path.join(fields_dir, f"{field_name}.field-meta.xml")
                    with open(field_file, 'w') as f:
                        f.write(field_xml)
                    
                    self.stats['fields_created'] += 1
                    logger.debug(f"Created field metadata: {field_file}")
                    
                except Exception as e:
                    logger.error(f"Error generating metadata for field {field.get('name', 'unknown')}: {str(e)}")
                    self.stats['errors'] += 1
            
            self.stats['objects_processed'] += 1

    def _generate_custom_object_metadata(self, obj_name: str, obj_config: Dict[str, Any]):
        """Generate metadata XML for a custom object."""
        label = obj_config.get('label', obj_name.replace('__c', '').replace('_', ' '))
        
        # Create custom object XML
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>{obj_name}</fullName>
    <label>{label}</label>
    <pluralLabel>{label}s</pluralLabel>
    <deploymentStatus>Deployed</deploymentStatus>
    <sharingModel>ReadWrite</sharingModel>
    <externalSharingModel>Private</externalSharingModel>
    <nameField>
        <label>Name</label>
        <type>Text</type>
    </nameField>
    <allowInChatterGroups>true</allowInChatterGroups>
    <enableSearch>true</enableSearch>
    <enableActivities>true</enableActivities>
    <enableReports>true</enableReports>
</CustomObject>
"""
        
        # Write to file
        object_file = os.path.join(self.objects_dir, f"{obj_name}/{obj_name}.object-meta.xml")
        os.makedirs(os.path.dirname(object_file), exist_ok=True)
        
        with open(object_file, 'w') as f:
            f.write(xml)
        
        logger.debug(f"Created custom object metadata: {object_file}")

    def _generate_field_xml(self, field_name: str, field_type: str, field_values: List[str], 
                           reference_to: str = None, formula: str = None, formula_return_type: str = None) -> str:
        """Generate the XML for a field based on its type."""
        # Basic field properties
        field_label = field_name.replace('__c', '').replace('_', ' ')
        
        # Start XML
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>{field_name}</fullName>
    <label>{field_label}</label>
"""
        
        # Add type-specific XML
        if field_type == 'Text':
            xml += """    <type>Text</type>
    <length>255</length>
"""
        elif field_type == 'Long Text Area':
            xml += """    <type>LongTextArea</type>
    <length>32000</length>
    <visibleLines>5</visibleLines>
"""
        elif field_type == 'Checkbox':
            xml += """    <type>Checkbox</type>
    <defaultValue>false</defaultValue>
"""
        elif field_type == 'Number':
            xml += """    <type>Number</type>
    <precision>18</precision>
    <scale>0</scale>
"""
        elif field_type == 'Percent':
            xml += """    <type>Percent</type>
    <precision>18</precision>
    <scale>2</scale>
"""
        elif field_type == 'Currency':
            xml += """    <type>Currency</type>
    <precision>18</precision>
    <scale>2</scale>
"""
        elif field_type == 'Date':
            xml += """    <type>Date</type>
"""
        elif field_type == 'DateTime':
            xml += """    <type>DateTime</type>
"""
        elif field_type == 'Email':
            xml += """    <type>Email</type>
"""
        elif field_type == 'Phone':
            xml += """    <type>Phone</type>
"""
        elif field_type == 'URL':
            xml += """    <type>Url</type>
"""
        elif field_type == 'TextArea':
            xml += """    <type>TextArea</type>
"""
        elif field_type == 'Picklist':
            xml += """    <type>Picklist</type>
    <valueSet>
        <restricted>true</restricted>
        <valueSetDefinition>
"""
            for value in field_values:
                xml += f"""            <value>
                <fullName>{value}</fullName>
                <default>false</default>
                <label>{value}</label>
            </value>
"""
            xml += """        </valueSetDefinition>
    </valueSet>
"""
        elif field_type == 'Multi-Picklist':
            xml += """    <type>MultiselectPicklist</type>
    <valueSet>
        <restricted>true</restricted>
        <valueSetDefinition>
"""
            for value in field_values:
                xml += f"""            <value>
                <fullName>{value}</fullName>
                <default>false</default>
                <label>{value}</label>
            </value>
"""
            xml += """        </valueSetDefinition>
    </valueSet>
    <visibleLines>4</visibleLines>
"""
        elif field_type == 'Lookup':
            # Remove __c from the reference name if it's there
            ref_obj = reference_to
            if ref_obj and ref_obj.endswith('__c'):
                ref_obj = ref_obj[:-3]
                
            relationship_name = field_name.replace('__c', '')
            xml += f"""    <type>Lookup</type>
    <referenceTo>{reference_to}</referenceTo>
    <relationshipName>{relationship_name}</relationshipName>
    <relationshipLabel>{field_label}</relationshipLabel>
"""
        elif field_type == 'Formula':
            # Use provided formula values or defaults
            formula_value = formula or "1"  # Default to 1 if no formula provided
            formula_type = formula_return_type or "Text"  # Default to Text
            
            xml += f"""    <type>Formula</type>
    <formula>{formula_value}</formula>
    <formulaTreatBlanksAs>BlankAsZero</formulaTreatBlanksAs>
    <returnType>{formula_type}</returnType>
"""
        else:
            # Default to Text for unknown types
            logger.warning(f"Unknown field type: {field_type}. Defaulting to Text.")
            xml += """    <type>Text</type>
    <length>255</length>
"""
        
        # Close XML
        xml += "</CustomField>"
        
        return xml

    def _generate_workflow_metadata(self):
        """Generate metadata for workflow rules."""
        workflow_rules = self.config.get('workflowRules', {})
        
        if not workflow_rules:
            logger.info("No workflow rules to process")
            return
        
        # Group workflow rules by object
        object_workflows = {}
        
        for rule_name, rule_config in workflow_rules.items():
            # Identify the object from the rule criteria or actions
            object_name = self._identify_workflow_object(rule_name, rule_config)
            
            if not object_name:
                logger.warning(f"Could not identify object for workflow rule: {rule_name}")
                continue
            
            if object_name not in object_workflows:
                object_workflows[object_name] = []
            
            object_workflows[object_name].append((rule_name, rule_config))
        
        # Generate workflow XML for each object
        for object_name, rules in object_workflows.items():
            self._generate_object_workflow_metadata(object_name, rules)

    def _identify_workflow_object(self, rule_name: str, rule_config: Dict[str, Any]) -> Optional[str]:
        """Identify the object a workflow rule applies to."""
        # Try to parse from the rule criteria
        criteria = rule_config.get('criteria', '')
        
        # Look for object reference in criteria (e.g., "Account.field")
        object_match = re.search(r'(\w+)\.', criteria)
        if object_match:
            return object_match.group(1)
        
        # Look for field references in actions
        for action in rule_config.get('actions', []):
            field = action.get('field', '')
            field_match = re.search(r'(\w+)\.', field)
            if field_match:
                return field_match.group(1)
        
        # Try to guess from the rule name
        for obj_name in self.config.get('objects', {}):
            if obj_name in rule_name:
                return obj_name
        
        # Default to Case if we can't determine
        return "Case"

    def _generate_object_workflow_metadata(self, object_name: str, rules: List[Tuple[str, Dict[str, Any]]]):
        """Generate workflow metadata XML for an object."""
        # Create workflows directory if it doesn't exist
        os.makedirs(self.workflows_dir, exist_ok=True)
        
        # Start XML
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Workflow xmlns="http://soap.sforce.com/2006/04/metadata">
"""
        
        # Add each rule
        for rule_name, rule_config in rules:
            description = rule_config.get('description', '')
            criteria = rule_config.get('criteria', '')
            actions = rule_config.get('actions', [])
            
            xml += f"""    <rules>
        <fullName>{rule_name}</fullName>
        <active>true</active>
        <description>{description}</description>
        <formula>{criteria}</formula>
        <triggerType>onCreateOrTriggeringUpdate</triggerType>
"""
            
            # Add actions
            for action in actions:
                action_type = action.get('type', '')
                
                if action_type == 'FieldUpdate':
                    field = action.get('field', '')
                    value = action.get('value', '')
                    
                    xml += f"""        <actions>
            <name>Update_{field.replace('.', '_')}</name>
            <type>FieldUpdate</type>
        </actions>
"""
                elif action_type == 'Notify':
                    recipient = action.get('recipient', '')
                    
                    xml += f"""        <actions>
            <name>Notify_{recipient}</name>
            <type>Alert</type>
        </actions>
"""
                # Add more action types as needed
                
            xml += "    </rules>\n"
            
            self.stats['workflow_rules_created'] += 1
            logger.debug(f"Added workflow rule: {rule_name}")
        
        # Close XML
        xml += "</Workflow>"
        
        # Write to file
        workflow_file = os.path.join(self.workflows_dir, f"{object_name}.workflow-meta.xml")
        with open(workflow_file, 'w') as f:
            f.write(xml)
        
        logger.info(f"Created workflow metadata for {object_name} with {len(rules)} rules")

    def _generate_dashboard_metadata(self):
        """Generate metadata for dashboards."""
        dashboards = self.config.get('dashboards', {})
        
        if not dashboards:
            logger.info("No dashboards to process")
            return
        
        # Create dashboards directories
        for dashboard_name, dashboard_config in dashboards.items():
            try:
                # Create folder structure
                dashboard_dir = os.path.join(self.dashboards_dir, dashboard_name)
                os.makedirs(dashboard_dir, exist_ok=True)
                
                # Generate dashboard XML
                dashboard_xml = self._generate_dashboard_xml(dashboard_name, dashboard_config)
                
                # Write to file
                dashboard_file = os.path.join(dashboard_dir, f"{dashboard_name}.dashboard-meta.xml")
                with open(dashboard_file, 'w') as f:
                    f.write(dashboard_xml)
                
                self.stats['dashboards_created'] += 1
                logger.info(f"Created dashboard metadata: {dashboard_name}")
            
            except Exception as e:
                logger.error(f"Error generating dashboard {dashboard_name}: {str(e)}")
                self.stats['errors'] += 1

    def _generate_dashboard_xml(self, dashboard_name: str, dashboard_config: Dict[str, Any]) -> str:
        """Generate the XML for a dashboard."""
        # Simple dashboard XML template
        widgets = dashboard_config.get('widgets', [])
        
        # Start XML
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Dashboard xmlns="http://soap.sforce.com/2006/04/metadata">
    <backgroundEndColor>#FFFFFF</backgroundEndColor>
    <backgroundFadeDirection>Diagonal</backgroundFadeDirection>
    <backgroundStartColor>#FFFFFF</backgroundStartColor>
    <dashboardType>SpecifiedUser</dashboardType>
    <isGridLayout>true</isGridLayout>
    <leftSection>
        <columnSize>Medium</columnSize>
"""
        
        # Add widgets
        for i, widget in enumerate(widgets):
            widget_type = widget.get('type', '')
            title = widget.get('title', f'Widget {i+1}')
            source = widget.get('source', '')
            
            xml += f"""        <dashboardComponents>
            <chartAxisRange>Auto</chartAxisRange>
            <componentType>{self._map_widget_type(widget_type)}</componentType>
            <displayUnits>Auto</displayUnits>
            <header>{title}</header>
"""
            
            if widget_type in ['Chart', 'Table']:
                xml += f"""            <reportName>{title.replace(' ', '_')}_Report</reportName>
"""
            
            xml += """        </dashboardComponents>
"""
        
        # Close XML
        xml += """    </leftSection>
    <runningUser>admin@example.com</runningUser>
    <textColor>#000000</textColor>
    <title>{title}</title>
    <titleColor>#000000</titleColor>
    <titleSize>12</titleSize>
</Dashboard>
"""
        
        return xml

    def _map_widget_type(self, widget_type: str) -> str:
        """Map widget types to Salesforce component types."""
        type_map = {
            'Metric': 'Metric',
            'Chart': 'Chart',
            'Table': 'Table',
            'Gauge': 'Gauge'
        }
        return type_map.get(widget_type, 'Table')

    def _generate_lightningflow_metadata(self):
        """Generate metadata for Lightning Flows."""
        lightning_flows = self.config.get('lightningFlows', {})
        
        if not lightning_flows:
            logger.debug("No Lightning Flows to process")
            return
        
        # Create flows directory
        flows_dir = os.path.join(self.metadata_dir, 'flows')
        os.makedirs(flows_dir, exist_ok=True)
        
        for flow_name, flow_config in lightning_flows.items():
            try:
                logger.info(f"Generating Lightning Flow: {flow_name}")
                
                # Generate basic flow XML
                flow_xml = self._generate_flow_xml(flow_name, flow_config)
                
                # Write to file
                flow_file = os.path.join(flows_dir, f"{flow_name}.flow-meta.xml")
                with open(flow_file, 'w') as f:
                    f.write(flow_xml)
                
                logger.debug(f"Created Lightning Flow metadata: {flow_file}")
            
            except Exception as e:
                logger.error(f"Error generating Lightning Flow {flow_name}: {str(e)}")
                self.stats['errors'] += 1

    def _generate_flow_xml(self, flow_name: str, flow_config: Dict[str, Any]) -> str:
        """Generate basic XML for a Lightning Flow."""
        description = flow_config.get('description', '')
        
        # Generate a very basic flow XML (placeholder)
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>63.0</apiVersion>
    <description>{description}</description>
    <label>{flow_name}</label>
    <status>Draft</status>
</Flow>
"""
        return xml

    def _generate_service_console_metadata(self):
        """Generate metadata for Service Console components."""
        service_console = self.config.get('serviceConsole', {})
        
        if not service_console:
            logger.debug("No Service Console components to process")
            return
        
        # This would normally create flexipage or console app metadata
        # For now, just log that we would create these
        logger.info(f"Service Console configuration found with {len(service_console.get('components', {}))} components")
        logger.info("Note: Service Console metadata generation is a placeholder - would create flexipage metadata")

    def _create_package_xml(self):
        """Create the package.xml file for deployment."""
        # Determine which metadata types to include
        metadata_types = []
        
        # Check objects and fields
        if self.config.get('objects'):
            has_custom_objects = any(obj_name.endswith('__c') for obj_name in self.config.get('objects', {}))
            if has_custom_objects:
                metadata_types.append(("CustomObject", ["*"]))
            
            metadata_types.append(("CustomField", ["*"]))
        
        # Check workflows
        if self.config.get('workflowRules'):
            metadata_types.append(("Workflow", ["*"]))
        
        # Check dashboards
        if self.config.get('dashboards'):
            metadata_types.append(("Dashboard", ["*"]))
        
        # Check lightning flows
        if self.config.get('lightningFlows'):
            metadata_types.append(("Flow", ["*"]))
        
        # Additional components from rich schema
        if self.config.get('serviceConsole'):
            metadata_types.append(("FlexiPage", ["*"]))
        
        # Start XML
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
"""
        
        # Add metadata types
        for metadata_type, members in metadata_types:
            xml += f"    <types>\n"
            for member in members:
                xml += f"        <members>{member}</members>\n"
            xml += f"        <name>{metadata_type}</name>\n"
            xml += f"    </types>\n"
        
        # Close XML
        xml += """    <version>63.0</version>
</Package>
"""
        
        # Write to file
        package_file = os.path.join(self.metadata_dir, 'package.xml')
        with open(package_file, 'w') as f:
            f.write(xml)
        
        logger.info(f"Created package.xml with {len(metadata_types)} metadata types")

    def deploy_metadata(self, deploy: bool = True) -> bool:
        """
        Deploy the metadata using Salesforce CLI.
        
        Args:
            deploy: If False, only validate without deploying
            
        Returns:
            True if deployment was successful, False otherwise
        """
        if not deploy:
            logger.info("Skipping deployment (--no-deploy flag set)")
            return True
        
        logger.info("Deploying metadata using Salesforce CLI...")
        
        # Find Salesforce CLI
        sf_cmd = self._find_sf_cli()
        if not sf_cmd:
            logger.error("Salesforce CLI not found. Please ensure it's installed.")
            return False
        
        # Authenticate to Salesforce
        auth_success = self._authenticate_salesforce(sf_cmd)
        if not auth_success:
            return False
        
        # Change to deploy directory
        original_dir = os.getcwd()
        os.chdir(self.deploy_dir)
        logger.debug(f"Changed working directory to: {self.deploy_dir}")
        
        try:
            # Deploy command
            deploy_cmd = [
                sf_cmd,
                'project', 'deploy', 'start',
                '--source-dir', 'force-app',
                '--target-org', 'sfdeployer',
                '--wait', '30',
                '--verbose'
            ]
            
            # Log the command being executed
            logger.info(f"Executing deployment command: {' '.join(deploy_cmd)}")
            
            # Execute the deployment
            start_time = datetime.now()
            
            try:
                # Run the deployment command
                deployment = subprocess.run(
                    deploy_cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                # Log success
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.info(f"Deployment successful! Duration: {duration:.2f} seconds")
                logger.info(f"Deployment output:\n{deployment.stdout}")
                return True
                
            except subprocess.CalledProcessError as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.error(f"Deployment failed after {duration:.2f} seconds")
                
                # Log error details
                logger.error(f"Error code: {e.returncode}")
                if e.stdout:
                    logger.error(f"Standard output: {e.stdout}")
                if e.stderr:
                    logger.error(f"Error output: {e.stderr}")
                
                # Extract component errors if available
                self._extract_deployment_errors(e.stdout, e.stderr)
                
                return False
                
        finally:
            # Always change back to the original directory
            os.chdir(original_dir)
            logger.debug(f"Changed working directory back to: {original_dir}")

    def _extract_deployment_errors(self, stdout: str, stderr: str):
        """Extract and log specific component errors from deployment output."""
        # Search for component failures in the output
        component_errors = re.findall(r'Error: (.*?): (.*?)(?=\n|$)', stderr or stdout or '')
        
        if component_errors:
            logger.error("Specific component errors:")
            for component, error in component_errors:
                logger.error(f"  - {component}: {error}")

    def _find_sf_cli(self) -> Optional[str]:
        """Find the Salesforce CLI executable."""
        # Common locations for the Salesforce CLI
        possible_locations = [
            "sf",  # if in PATH
            "sfdx",  # legacy command if in PATH
            r"C:\Program Files\sf\client\bin\sf.cmd",  # Windows default
            r"C:\Program Files\sfdx\client\bin\sfdx.cmd",  # Windows legacy
            "/usr/local/bin/sf",  # macOS/Linux common location
            os.path.expanduser("~/.local/bin/sf")  # User local bin
        ]
        
        # Try each location
        for location in possible_locations:
            try:
                # Check if command exists and is runnable
                subprocess.run([location, "--version"], capture_output=True, text=True, check=False)
                logger.info(f"Found Salesforce CLI at: {location}")
                return location
            except (subprocess.SubprocessError, FileNotFoundError):
                continue
        
        logger.error("Salesforce CLI not found in any standard location.")
        logger.error("Please install the Salesforce CLI using: npm install -g @salesforce/cli")
        return None

    def _authenticate_salesforce(self, sf_cmd: str) -> bool:
        """Authenticate to Salesforce using environment credentials."""
        # Get credentials from environment
        username = os.getenv('SF_USERNAME')
        password = os.getenv('SF_PASSWORD')
        security_token = os.getenv('SF_SECURITY_TOKEN', '')
        instance_url = os.getenv('SF_INSTANCE_URL') or os.getenv('SF_LOGIN_URL') or "https://login.salesforce.com"
        
        # Make sure instance URL has https://
        if not instance_url.startswith('https://'):
            instance_url = f"https://{instance_url}"
        
        logger.info(f"Authenticating to Salesforce as {username} at {instance_url}")
        
        # Authentication method 1: Web-based login
        try:
            logger.info("Attempting web-based authentication...")
            
            auth_cmd = [
                sf_cmd, 'org', 'login', 'web',
                '--instance-url', instance_url,
                '--alias', 'sfdeployer',
                '--set-default'
            ]
            
            auth_process = subprocess.run(
                auth_cmd,
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=60  # 1 minute timeout
            )
            
            logger.info("Web authentication successful!")
            return True
            
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.warning(f"Web authentication failed: {str(e)}")
            
            # Authentication method 2: Username/password
            try:
                logger.info("Attempting username/password authentication...")
                
                # Combine password and security token if provided
                auth_password = f"{password}{security_token}" if security_token else password
                
                auth_cmd = [
                    sf_cmd, 'org', 'login', 'username',
                    '--username', username,
                    '--password', auth_password,
                    '--instance-url', instance_url,
                    '--alias', 'sfdeployer',
                    '--set-default'
                ]
                
                auth_process = subprocess.run(
                    auth_cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                logger.info("Username/password authentication successful!")
                return True
                
            except subprocess.SubprocessError as e:
                logger.error(f"Username/password authentication failed: {str(e)}")
                logger.error("Authentication to Salesforce failed. Please check your credentials.")
                
                # Provide guidance on alternatives
                logger.error("\nAuthentication alternatives:")
                logger.error("1. Manually authenticate using: sf org login web")
                logger.error("2. Use sf org login sfdx-url with a pre-authenticated URL")
                logger.error("3. For CI/CD, use sf org login jwt with certificate authentication\n")
                
                return False

    def cleanup(self):
        """Clean up temporary files and directories."""
        logger.info("Cleaning up deployment files...")
        
        try:
            # Don't delete if using a user-specified output directory
            if os.path.exists(self.deploy_dir) and self.deploy_dir.startswith(tempfile.gettempdir()):
                shutil.rmtree(self.deploy_dir)
                logger.info(f"Removed temporary directory: {self.deploy_dir}")
            else:
                logger.info(f"Kept output directory: {self.deploy_dir}")
        except Exception as e:
            logger.warning(f"Error during cleanup: {str(e)}")
    
    def summarize_deployment(self):
        """Summarize the deployment operation."""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        # Create a summary report
        summary = f"""
==========================================================
                DEPLOYMENT SUMMARY
==========================================================
Start time:          {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
End time:            {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Duration:            {duration:.2f} seconds
Configuration file:  {self.config_path}
Output directory:    {self.deploy_dir}

Components processed:
  - Objects:         {self.stats['objects_processed']}
  - Fields:          {self.stats['fields_created']}
  - Workflow Rules:  {self.stats['workflow_rules_created']}
  - Dashboards:      {self.stats['dashboards_created']}
  
Errors encountered:  {self.stats['errors']}
==========================================================
"""
        
        logger.info(summary)
        
        # Create a summary file
        summary_file = f"salesforce_deploy_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(summary_file, 'w') as f:
            f.write(summary)
        
        logger.info(f"Summary written to: {summary_file}")
        return summary


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(
        description="Deploy Salesforce configuration from a JSON schema file using Metadata API"
    )
    
    parser.add_argument(
        '--config', 
        type=str, 
        default='config.json',
        help='Path to the JSON configuration file (default: config.json)'
    )
    
    parser.add_argument(
        '--env', 
        type=str, 
        default='.env',
        help='Path to the .env file with credentials (default: .env)'
    )
    
    parser.add_argument(
        '--output', 
        type=str, 
        default=None,
        help='Path to store deployment files (default: temporary directory)'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--no-deploy', 
        action='store_true',
        help='Generate metadata files without deploying'
    )
    
    parser.add_argument(
        '--validate', 
        action='store_true',
        help='Validate the JSON structure without deployment'
    )
    
    args = parser.parse_args()
    
    # Configure verbose logging if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    try:
        logger.info(f"Starting Salesforce deployment with configuration: {args.config}")
        
        # Create the deployer
        deployer = SalesforceDeployer(args.config, args.output, args.env)
        
        # If validation only, exit after initialization
        if args.validate:
            logger.info("Configuration validated successfully. Exiting without deployment.")
            deployer.summarize_deployment()
            return
        
        # Generate metadata
        deployer.generate_metadata()
        
        # Deploy metadata (skip if --no-deploy)
        if not args.no_deploy:
            success = deployer.deploy_metadata()
            
            if success:
                logger.info("✅ Deployment completed successfully!")
            else:
                logger.error("❌ Deployment failed!")
                deployer.summarize_deployment()
                sys.exit(1)
        
        # Summarize deployment
        deployer.summarize_deployment()
        
        # Clean up if successful
        if not args.output:  # Only clean up if using temp directory
            deployer.cleanup()
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid value or configuration: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()