class FieldMetadataGenerator:
    """Generates metadata for Salesforce fields."""

    def __init__(self, field_name: str, field_type: str, field_values: list = None, 
                 reference_to: str = None, formula: str = None, formula_return_type: str = None):
        self.field_name = field_name
        self.field_type = field_type
        self.field_values = field_values or []
        self.reference_to = reference_to
        self.formula = formula
        self.formula_return_type = formula_return_type

    def generate_metadata(self) -> str:
        """Generate the XML metadata for the field."""
        xml = self._generate_field_xml()
        return xml

    def _generate_field_xml(self) -> str:
        """Generate the XML for the field based on its type."""
        field_label = self.field_name.replace('__c', '').replace('_', ' ')
        
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>{self.field_name}</fullName>
    <label>{field_label}</label>
"""

        if self.field_type == 'Text':
            xml += """    <type>Text</type>
    <length>255</length>
"""
        elif self.field_type == 'Long Text Area':
            xml += """    <type>LongTextArea</type>
    <length>32000</length>
    <visibleLines>5</visibleLines>
"""
        elif self.field_type == 'Checkbox':
            xml += """    <type>Checkbox</type>
    <defaultValue>false</defaultValue>
"""
        elif self.field_type == 'Number':
            xml += """    <type>Number</type>
    <precision>18</precision>
    <scale>0</scale>
"""
        elif self.field_type == 'Percent':
            xml += """    <type>Percent</type>
    <precision>18</precision>
    <scale>2</scale>
"""
        elif self.field_type == 'Currency':
            xml += """    <type>Currency</type>
    <precision>18</precision>
    <scale>2</scale>
"""
        elif self.field_type == 'Date':
            xml += """    <type>Date</type>
"""
        elif self.field_type == 'DateTime':
            xml += """    <type>DateTime</type>
"""
        elif self.field_type == 'Email':
            xml += """    <type>Email</type>
"""
        elif self.field_type == 'Phone':
            xml += """    <type>Phone</type>
"""
        elif self.field_type == 'URL':
            xml += """    <type>Url</type>
"""
        elif self.field_type == 'TextArea':
            xml += """    <type>TextArea</type>
"""
        elif self.field_type == 'Picklist':
            xml += """    <type>Picklist</type>
    <valueSet>
        <restricted>true</restricted>
        <valueSetDefinition>
"""
            for value in self.field_values:
                xml += f"""            <value>{value}</value>
"""
            xml += """        </valueSetDefinition>
    </valueSet>
"""
        elif self.field_type == 'Multi-Picklist':
            xml += """    <type>MultiselectPicklist</type>
    <valueSet>
        <restricted>true</restricted>
        <valueSetDefinition>
"""
            for value in self.field_values:
                xml += f"""            <value>{value}</value>
"""
            xml += """        </valueSetDefinition>
    </valueSet>
    <visibleLines>4</visibleLines>
"""
        elif self.field_type == 'Lookup':
            ref_obj = self.reference_to
            if ref_obj and ref_obj.endswith('__c'):
                ref_obj = ref_obj[:-3]
            relationship_name = self.field_name.replace('__c', '')
            xml += f"""    <type>Lookup</type>
    <referenceTo>{self.reference_to}</referenceTo>
    <relationshipName>{relationship_name}</relationshipName>
    <relationshipLabel>{field_label}</relationshipLabel>
"""
        elif self.field_type == 'Formula':
            formula_value = self.formula or "1"
            formula_type = self.formula_return_type or "Text"
            xml += f"""    <type>Formula</type>
    <formula>{formula_value}</formula>
    <returnType>{formula_type}</returnType>
"""
        else:
            xml += """    <type>Text</type>
    <length>255</length>
"""

        xml += "</CustomField>"
        return xml