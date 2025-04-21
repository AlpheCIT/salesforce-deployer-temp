from typing import Dict, Any, List, Tuple
import os
import logging

logger = logging.getLogger(__name__)

class WorkflowMetadataGenerator:
    """Class to generate metadata for Salesforce workflow rules."""

    def __init__(self, config: Dict[str, Any], output_dir: str):
        self.config = config
        self.output_dir = output_dir
        self.workflow_dir = os.path.join(self.output_dir, 'workflows')
        os.makedirs(self.workflow_dir, exist_ok=True)

    def generate_workflow_metadata(self) -> None:
        """Generate workflow metadata files based on the configuration."""
        workflow_rules = self.config.get('workflowRules', {})
        
        if not workflow_rules:
            logger.info("No workflow rules to process")
            return
        
        for rule_name, rule_config in workflow_rules.items():
            self._generate_workflow_file(rule_name, rule_config)

    def _generate_workflow_file(self, rule_name: str, rule_config: Dict[str, Any]) -> None:
        """Generate a single workflow metadata file."""
        xml_content = self._create_workflow_xml(rule_name, rule_config)
        file_path = os.path.join(self.workflow_dir, f"{rule_name}.workflow-meta.xml")
        
        with open(file_path, 'w') as f:
            f.write(xml_content)
        
        logger.info(f"Created workflow metadata file: {file_path}")

    def _create_workflow_xml(self, rule_name: str, rule_config: Dict[str, Any]) -> str:
        """Create the XML representation of a workflow rule."""
        description = rule_config.get('description', '')
        criteria = rule_config.get('criteria', '')
        actions = rule_config.get('actions', [])

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Workflow xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>{rule_name}</fullName>
    <active>true</active>
    <description>{description}</description>
    <formula>{criteria}</formula>
    <triggerType>onCreateOrTriggeringUpdate</triggerType>
    <rules>
"""

        for action in actions:
            action_type = action.get('type', '')
            action_details = action.get('details', {})
            xml += f"        <action>\n            <type>{action_type}</type>\n"
            for key, value in action_details.items():
                xml += f"            <{key}>{value}</{key}>\n"
            xml += "        </action>\n"

        xml += """    </rules>
</Workflow>
"""
        return xml