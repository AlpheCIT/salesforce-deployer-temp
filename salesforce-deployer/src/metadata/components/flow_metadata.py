class FlowMetadataGenerator:
    """Generates metadata for Salesforce flows."""

    def __init__(self, flow_name: str, flow_config: dict):
        self.flow_name = flow_name
        self.flow_config = flow_config

    def generate_flow_xml(self) -> str:
        """Generate the XML for the flow."""
        description = self.flow_config.get('description', '')
        
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>63.0</apiVersion>
    <description>{description}</description>
    <label>{self.flow_name}</label>
    <status>Draft</status>
</Flow>
"""
        return xml

    def save_flow_metadata(self, output_dir: str):
        """Save the generated flow metadata XML to a file."""
        flow_xml = self.generate_flow_xml()
        flow_file_path = f"{output_dir}/{self.flow_name}.flow-meta.xml"
        
        with open(flow_file_path, 'w') as flow_file:
            flow_file.write(flow_xml)