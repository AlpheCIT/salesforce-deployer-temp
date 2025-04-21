from typing import Dict, Any

class ObjectMetadataGenerator:
    """Class to generate metadata for Salesforce objects."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate_metadata(self) -> None:
        """Generate metadata for all objects defined in the configuration."""
        objects = self.config.get('objects', {})
        for obj_name, obj_config in objects.items():
            self._generate_object_metadata(obj_name, obj_config)

    def _generate_object_metadata(self, obj_name: str, obj_config: Dict[str, Any]) -> None:
        """Generate metadata for a single object."""
        # Logic to create object metadata XML
        label = obj_config.get('label', obj_name.replace('__c', '').replace('_', ' '))
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
        # Write XML to file (implementation not shown)
        self._write_metadata_to_file(obj_name, xml)

    def _write_metadata_to_file(self, obj_name: str, xml: str) -> None:
        """Write the generated XML to a file."""
        # Implementation for writing XML to a file goes here
        pass