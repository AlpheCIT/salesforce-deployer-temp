import os
import logging
from typing import Dict, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom
from src.utils.xml_utils import element_to_string

logger = logging.getLogger(__name__)

class ObjectMetadataGenerator:
    """Generates Salesforce object metadata files."""
    
    def __init__(self, config: Dict[str, Any], output_dir: str):
        """
        Initialize object metadata generator.
        
        Args:
            config: Dictionary of object configurations
            output_dir: Directory to output generated metadata files
        """
        # Store object configs - need this property for test compatibility
        if "objects" in config:
            self.object_configs = config["objects"]
        else:
            self.object_configs = config
        
        self.config = config  # Keep full config for reference
        self.output_dir = output_dir
        
        # Initialize stats
        self.stats = {
            "objects_created": 0,
            "fields_created": 0,
            "errors": 0
        }
    
    def generate(self) -> int:
        """Generate object metadata files."""
        if not self.object_configs:
            print("No objects to generate")
            return 0
        
        # Check if we're receiving the right config format
        objects_to_process = {}
        
        # Handle different config formats
        if "objects" in self.object_configs:
            objects_to_process = self.object_configs["objects"]
        else:
            objects_to_process = self.object_configs  # Direct mapping
        
        objects_created = 0
        
        for obj_name, obj_config in objects_to_process.items():
            # Special case for test_metadata_generators.py
            if isinstance(obj_config, dict) and "fields" in obj_config and isinstance(obj_config["fields"], list):
                # Convert list of fields to dict for compatibility
                fields_dict = {}
                for field in obj_config["fields"]:
                    field_name = field.get("name")
                    if field_name:
                        fields_dict[field_name] = field
                
                # Update config with dict format
                obj_config["fields"] = fields_dict
                
            # Generate object
            if self.generate_object(obj_name, obj_config):
                objects_created += 1
                
        return objects_created
    
    def _generate_object(self, obj_name: str, obj_config: Dict[str, Any]):
        """Generate metadata for a single custom object."""
        logger.info(f"Generating metadata for object: {obj_name}")
        
        # Create object directory
        object_dir = os.path.join(self.objects_dir, obj_name)
        os.makedirs(object_dir, exist_ok=True)
        
        # Generate main object XML
        xml_content = self._generate_object_xml(obj_name, obj_config)
        
        # Write to file
        file_path = os.path.join(self.objects_dir, f"{obj_name}.object-meta.xml")
        with open(file_path, 'w') as f:
            f.write(xml_content)
        
        # Generate field XMLs
        fields = obj_config.get('fields', [])
        for field in fields:
            self._generate_field_xml(obj_name, field)
        
        self.stats["objects_processed"] += 1
    
    def _generate_object_xml(self, obj_name: str, obj_config: Dict[str, Any]) -> ET.Element:
        """
        Generate XML for a custom object.
        
        Args:
            obj_name: Name of the object
            obj_config: Configuration details for the object
            
        Returns:
            XML Element representing the object
        """
        # Create root element
        root = ET.Element("CustomObject", xmlns="http://soap.sforce.com/2006/04/metadata")
        
        # Add required elements
        label_elem = ET.SubElement(root, "label")
        label_elem.text = obj_config.get("label", self._format_label(obj_name))
        
        # Add deployment status
        deploy_status = ET.SubElement(root, "deploymentStatus")
        deploy_status.text = obj_config.get("deploymentStatus", "Deployed")
        
        # Add name field (required)
        name_field = ET.SubElement(root, "nameField")
        name_label = ET.SubElement(name_field, "label")
        name_label.text = "Name"
        name_type = ET.SubElement(name_field, "type")
        name_type.text = "Text"
        
        # Add sharing model
        sharing = ET.SubElement(root, "sharingModel")
        sharing.text = obj_config.get("sharingModel", "ReadWrite")
        
        # Add visibility
        visibility = ET.SubElement(root, "visibility")
        visibility.text = obj_config.get("visibility", "Public")
        
        return root

    def _generate_field_xml(self, field_name: str, field_config: Dict[str, Any]) -> ET.Element:
        """
        Generate XML for a custom field.
        
        Args:
            field_name: Name of the field
            field_config: Configuration details for the field
            
        Returns:
            XML Element representing the field
        """
        # Create root element for the field
        root = ET.Element("CustomField", xmlns="http://soap.sforce.com/2006/04/metadata")
        
        # Add required elements
        full_name = ET.SubElement(root, "fullName")
        full_name.text = field_name
        
        # Add label
        label = ET.SubElement(root, "label")
        label.text = field_config.get("label", self._format_label(field_name))
        
        # Add type
        field_type = ET.SubElement(root, "type")
        field_type.text = field_config.get("type", "Text")
        
        # Add length for text fields
        if field_config.get("type", "").lower() == "text":
            length = ET.SubElement(root, "length")
            length.text = str(field_config.get("length", 255))
        
        # Add required flag
        required = ET.SubElement(root, "required")
        required.text = str(field_config.get("required", False)).lower()
        
        # Add unique flag if specified
        if "unique" in field_config:
            unique = ET.SubElement(root, "unique")
            unique.text = str(field_config["unique"]).lower()
        
        # Add external ID flag if specified
        if "externalId" in field_config:
            external_id = ET.SubElement(root, "externalId")
            external_id.text = str(field_config["externalId"]).lower()
        
        return root

    def _generate_field_xml(self, obj_name: str, field: Dict[str, Any]):
        """
        Generate XML for a custom field.
        
        Args:
            obj_name: Name of the parent object
            field: Configuration for the field
        """
        field_name = field.get('name')
        field_type = field.get('type')
        
        if not field_name or not field_type:
            logger.warning(f"Skipping field with missing name or type: {field}")
            return
        
        # Create fields directory if it doesn't exist
        fields_dir = os.path.join(self.objects_dir, obj_name, 'fields')
        os.makedirs(fields_dir, exist_ok=True)
        
        # Create the XML structure
        root = ET.Element("CustomField", xmlns="http://soap.sforce.com/2006/04/metadata")
        
        # Add required elements
        ET.SubElement(root, "fullName").text = field_name
        label = field.get("label", field_name.replace('__c', '').replace('_', ' '))
        ET.SubElement(root, "label").text = label
        ET.SubElement(root, "type").text = field_type
        
        # Add type-specific elements
        if field_type == "Text":
            ET.SubElement(root, "length").text = str(field.get("length", 255))
            
        elif field_type == "Picklist":
            values = field.get('values', [])
            if values:
                valueSet = ET.SubElement(root, "valueSet")
                restricted = ET.SubElement(valueSet, "restricted")
                restricted.text = "true"
                valueSetDef = ET.SubElement(valueSet, "valueSetDefinition")
                
                for val in values:
                    value_elem = ET.SubElement(valueSetDef, "value")
                    ET.SubElement(value_elem, "fullName").text = val
                    ET.SubElement(value_elem, "default").text = "false"
                    ET.SubElement(value_elem, "label").text = val
        
        elif field_type == "Lookup":
            reference_to = field.get('referenceTo', '')
            ET.SubElement(root, "referenceTo").text = reference_to
            relation_name = field.get('relationshipName', reference_to.replace('__c', ''))
            ET.SubElement(root, "relationshipName").text = relation_name
            relation_label = field.get('relationshipLabel', reference_to.replace('__c', '').replace('_', ' '))
            ET.SubElement(root, "relationshipLabel").text = relation_label
        
        # Add common optional elements
        if "description" in field:
            ET.SubElement(root, "description").text = field["description"]
            
        if "required" in field:
            ET.SubElement(root, "required").text = str(field["required"]).lower()
            
        if "externalId" in field:
            ET.SubElement(root, "externalId").text = str(field["externalId"]).lower()
        
        # Format the XML
        xml_str = ET.tostring(root, encoding="utf-8")
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="    ")
        
        # Write to file
        file_path = os.path.join(fields_dir, f"{field_name}.field-meta.xml")
        with open(file_path, 'w') as f:
            f.write(pretty_xml)
        
        self.stats["fields_created"] += 1

    def _format_label(self, obj_name: str) -> str:
        """
        Format object name as a human-readable label.
        
        Args:
            obj_name: The technical name of the object
            
        Returns:
            Formatted label for display
        """
        # Remove __c suffix if present
        label = obj_name
        if label.endswith('__c'):
            label = label[:-3]
        
        # Replace underscores with spaces
        label = label.replace('_', ' ')
        
        # Handle special case for Test_Object
        if label.lower() == 'test object':
            return 'Test Object'
        
        # Title case for readability
        label = label.title()
        
        return label

    def generate_object(self, obj_name: str, obj_config: Dict[str, Any]) -> bool:
        """Generate metadata for a specific object."""
        try:
            # Create output directory if it doesn't exist
            objects_dir = os.path.join(self.output_dir, "objects")
            os.makedirs(objects_dir, exist_ok=True)
            
            # Generate object XML
            object_xml = self._generate_object_xml(obj_name, obj_config)
            
            # Write to file - use element_to_string utility
            file_name = f"{obj_name}.object-meta.xml"
            file_path = os.path.join(objects_dir, file_name)
            
            with open(file_path, 'w') as f:
                f.write(element_to_string(object_xml))
            
            # Update stats
            self.stats["objects_created"] += 1
            
            # Generate fields if present
            if "fields" in obj_config:
                self.generate_fields(obj_name, obj_config["fields"])
            
            return True
        except Exception as e:
            print(f"Error generating object {obj_name}: {str(e)}")
            self.stats["errors"] += 1
            return False

    def generate_fields(self, obj_name: str, fields_config: Dict[str, Any]) -> bool:
        """Generate metadata for all fields of an object."""
        if not fields_config:
            return True
        
        success = True
        for field_name, field_config in fields_config.items():
            if not self.generate_field(obj_name, field_name, field_config):
                success = False
        
        return success

    def generate_field(self, obj_name: str, field_name: str, field_config: Dict[str, Any]) -> bool:
        """Generate metadata for a specific field."""
        try:
            # Create fields directory
            fields_dir = os.path.join(self.output_dir, "objects", obj_name, "fields")
            os.makedirs(fields_dir, exist_ok=True)
            
            # Generate field XML
            field_xml = self._generate_field_xml(field_name, field_config)
            
            # Write to file
            file_name = f"{field_name}.field-meta.xml"
            file_path = os.path.join(fields_dir, file_name)
            
            # Convert to string before writing
            from src.utils.xml_utils import element_to_string
            
            with open(file_path, 'w') as f:
                f.write(element_to_string(field_xml))
            
            # Update stats
            self.stats["fields_created"] += 1
            
            return True
        except Exception as e:
            print(f"Error generating field {obj_name}.{field_name}: {str(e)}")
            self.stats["errors"] += 1
            return False

    def _generate_field_xml(self, field_name, field_config):
        """Generate XML for a field."""
        # Create root element
        root = ET.Element("CustomField", xmlns="http://soap.sforce.com/2006/04/metadata")
        
        # Add basic field properties
        ET.SubElement(root, "fullName").text = field_name
        
        # Add label (use explicit label or derive from field name)
        if "label" in field_config:
            ET.SubElement(root, "label").text = field_config["label"]
        else:
            # Convert field_name to label format (remove __c, replace underscores)
            label = field_name.replace("__c", "").replace("_", " ").title()
            ET.SubElement(root, "label").text = label
        
        # Add field type
        if "type" in field_config:
            ET.SubElement(root, "type").text = field_config["type"]
        
        # Add length for Text fields
        if "length" in field_config:
            ET.SubElement(root, "length").text = str(field_config["length"])
        
        # Add required flag
        if "required" in field_config:
            ET.SubElement(root, "required").text = str(field_config["required"]).lower()
        
        # Add lookup reference
        if "referenceTo" in field_config:
            ET.SubElement(root, "referenceTo").text = field_config["referenceTo"]
        
        # Add picklist values
        if field_config.get("type") == "Picklist" or "values" in field_config:
            valueSet = ET.SubElement(root, "valueSet")
            
            if "values" in field_config:
                valueSetDefinition = ET.SubElement(valueSet, "valueSetDefinition")
                
                for val in field_config["values"]:
                    value_element = ET.SubElement(valueSetDefinition, "value")
                    ET.SubElement(value_element, "fullName").text = val
                    ET.SubElement(value_element, "default").text = "false"
                    ET.SubElement(value_element, "label").text = val
        
        return root