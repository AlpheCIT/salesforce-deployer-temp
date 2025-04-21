from typing import List, Tuple
import os
import xml.etree.ElementTree as ET

class PackageBuilder:
    def __init__(self, metadata_types: List[Tuple[str, List[str]]]):
        self.metadata_types = metadata_types

    def build_package_xml(self) -> str:
        package = ET.Element('Package', xmlns="http://soap.sforce.com/2006/04/metadata")
        
        for metadata_type, members in self.metadata_types:
            types_element = ET.SubElement(package, 'types')
            for member in members:
                member_element = ET.SubElement(types_element, 'members')
                member_element.text = member
            name_element = ET.SubElement(types_element, 'name')
            name_element.text = metadata_type
        
        version_element = ET.SubElement(package, 'version')
        version_element.text = '63.0'
        
        return ET.tostring(package, encoding='utf-8', xml_declaration=True).decode('utf-8')

    def save_package_xml(self, file_path: str):
        package_xml = self.build_package_xml()
        with open(file_path, 'w') as f:
            f.write(package_xml)

def main():
    # Example usage
    metadata_types = [
        ('CustomObject', ['Account', 'Contact']),
        ('CustomField', ['Account.Custom_Field__c']),
        ('Workflow', ['Account_Workflow']),
        ('Dashboard', ['Sales_Dashboard']),
        ('Flow', ['Sample_Flow'])
    ]
    
    builder = PackageBuilder(metadata_types)
    builder.save_package_xml(os.path.join('path_to_your_directory', 'package.xml'))

if __name__ == "__main__":
    main()