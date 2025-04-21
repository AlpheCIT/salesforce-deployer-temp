from typing import Dict, Any

class DashboardMetadataGenerator:
    """Class to generate metadata for Salesforce dashboards."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the DashboardMetadataGenerator with configuration.

        Args:
            config: Configuration dictionary containing dashboard details.
        """
        self.config = config

    def generate_dashboard_metadata(self) -> str:
        """Generate the XML metadata for the dashboard."""
        dashboard_name = self.config.get('name', 'Default Dashboard')
        dashboard_description = self.config.get('description', '')
        widgets = self.config.get('widgets', [])

        xml = self._generate_dashboard_xml(dashboard_name, dashboard_description, widgets)
        return xml

    def _generate_dashboard_xml(self, name: str, description: str, widgets: list) -> str:
        """Create the XML structure for the dashboard."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Dashboard xmlns="http://soap.sforce.com/2006/04/metadata">
    <title>{name}</title>
    <description>{description}</description>
    <dashboardType>SpecifiedUser</dashboardType>
    <isGridLayout>true</isGridLayout>
    <leftSection>
        <columnSize>Medium</columnSize>
"""

        for widget in widgets:
            widget_type = widget.get('type', 'Table')
            title = widget.get('title', 'Untitled Widget')
            source = widget.get('source', '')

            xml += f"""        <dashboardComponents>
            <componentType>{widget_type}</componentType>
            <header>{title}</header>
            <source>{source}</source>
        </dashboardComponents>
"""

        xml += """    </leftSection>
</Dashboard>
"""
        return xml