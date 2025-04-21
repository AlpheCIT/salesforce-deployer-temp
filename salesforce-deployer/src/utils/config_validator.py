"""
Configuration validator for Salesforce Schema Deployer.
Validates JSON schema configurations against expected formats.
"""

import json
import os
from typing import Dict, List, Any, Union, Optional

class ConfigValidator:
    def __init__(self, config):
        self.config = config

    def validate(self):
        self._validate_structure()
        self._validate_required_fields()

    def _validate_structure(self):
        if not isinstance(self.config, dict):
            raise ValueError("Configuration must be a JSON object")

        required_sections = ['objects']
        missing_sections = [section for section in required_sections if section not in self.config]

        if missing_sections:
            raise ValueError(f"Missing required sections in configuration: {', '.join(missing_sections)}")

    def _validate_required_fields(self):
        for obj_name, obj_config in self.config.get('objects', {}).items():
            if 'fields' not in obj_config:
                raise ValueError(f"Object '{obj_name}' is missing 'fields' section")

            for field in obj_config['fields']:
                if 'name' not in field or 'type' not in field:
                    raise ValueError(f"Field in object '{obj_name}' is missing 'name' or 'type'")

def validate_config(config: Optional[Dict[str, Any]] = None, config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate a Salesforce configuration schema.
    
    Args:
        config: Dictionary containing the configuration to validate
        config_file: Path to a JSON file containing the configuration (used if config is None)
    
    Returns:
        Dictionary with validation results:
        {
            "valid": True/False,
            "errors": [list of error messages]
        }
    """
    errors = []
    
    # Load configuration from file if provided
    if config is None and config_file is not None:
        if not os.path.exists(config_file):
            return {"valid": False, "errors": [f"Config file not found: {config_file}"]}
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            return {"valid": False, "errors": [f"Invalid JSON in config file: {e}"]}
    
    # Check if we have a config to validate
    if config is None:
        return {"valid": False, "errors": ["No configuration provided"]}
    
    # Validate objects section if exists
    if "objects" in config:
        errors.extend(_validate_objects(config["objects"]))
    
    # Validate workflowRules section if exists
    if "workflowRules" in config:
        errors.extend(_validate_workflow_rules(config["workflowRules"]))
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

def _validate_objects(objects: Dict[str, Any]) -> List[str]:
    """Validate the objects section of the configuration."""
    errors = []
    
    for obj_name, obj_config in objects.items():
        # Validate required object fields
        if not isinstance(obj_config, dict):
            errors.append(f"Object '{obj_name}' must be a dictionary")
            continue
        
        # Check required object properties
        if "label" not in obj_config:
            errors.append(f"Object '{obj_name}' is missing required 'label' property")
        
        # Validate fields if present
        if "fields" in obj_config:
            if not isinstance(obj_config["fields"], list):
                errors.append(f"Fields for object '{obj_name}' must be a list")
            else:
                # Check each field
                field_names = set()
                for field in obj_config["fields"]:
                    if not isinstance(field, dict):
                        errors.append(f"Field in object '{obj_name}' must be a dictionary")
                        continue
                    
                    # Check required field properties
                    if "name" not in field:
                        errors.append(f"Field in object '{obj_name}' is missing required 'name' property")
                    else:
                        # Check for duplicate field names
                        field_name = field["name"]
                        if field_name in field_names:
                            errors.append(f"Duplicate field name '{field_name}' in object '{obj_name}'")
                        field_names.add(field_name)
                    
                    if "type" not in field:
                        errors.append(f"Field in object '{obj_name}' is missing required 'type' property")
                    else:
                        # Validate field type
                        field_type = field["type"]
                        valid_types = [
                            "Text", "LongTextArea", "Html", "RichTextArea", "Email", "Phone", 
                            "Url", "Number", "Percent", "Currency", "Date", "DateTime", 
                            "Checkbox", "Picklist", "MultiselectPicklist", "Lookup", "MasterDetail"
                        ]
                        if field_type not in valid_types:
                            errors.append(f"Unknown field type '{field_type}' in object '{obj_name}'")
                        
                        # Type-specific validations
                        if field_type in ["Lookup", "MasterDetail"]:
                            if "referenceTo" not in field:
                                errors.append(f"Field of type '{field_type}' requires 'referenceTo' in object '{obj_name}'")
    
    return errors

def _validate_workflow_rules(workflows: Dict[str, Any]) -> List[str]:
    """Validate the workflowRules section of the configuration."""
    errors = []
    
    for wf_name, wf_config in workflows.items():
        # Validate required workflow fields
        if not isinstance(wf_config, dict):
            errors.append(f"Workflow rule '{wf_name}' must be a dictionary")
            continue
        
        # Check required properties
        if "criteria" not in wf_config:
            errors.append(f"Workflow rule '{wf_name}' is missing required 'criteria' property")
        
        # Validate actions if present
        if "actions" in wf_config:
            if not isinstance(wf_config["actions"], list):
                errors.append(f"Actions for workflow '{wf_name}' must be a list")
            else:
                # Check each action
                for action in wf_config["actions"]:
                    if not isinstance(action, dict):
                        errors.append(f"Action in workflow '{wf_name}' must be a dictionary")
                        continue
                    
                    # Check required action properties
                    if "type" not in action:
                        errors.append(f"Action in workflow '{wf_name}' is missing required 'type' property")
    
    return errors

# Alias for backward compatibility if needed
validate_schema = validate_config