#!/usr/bin/env python3
"""
Test data generator for Salesforce Schema Deployer.
Creates various test schemas with different complexity levels.
"""

import json
import os
import random
import uuid
from typing import Dict, List, Any

class TestDataGenerator:
    """Generate test data for the Salesforce Schema Deployer tests."""
    
    def __init__(self, output_dir: str = "tests/fixtures/schemas"):
        """Initialize the test data generator."""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Lists of possible field types, picklist values, etc.
        self.field_types = [
            "Text", "Number", "Date", "DateTime", "Checkbox", 
            "Picklist", "MultiselectPicklist", "LongTextArea", "Html", 
            "Currency", "Percent", "Phone", "Email", "Url"
        ]
        
        self.picklist_values = [
            ["High", "Medium", "Low"],
            ["New", "In Progress", "Completed", "Cancelled"],
            ["North", "South", "East", "West"],
            ["Red", "Green", "Blue", "Yellow", "Purple"],
            ["Yes", "No", "Maybe"]
        ]
        
        # Common fields for various object types
        self.common_field_templates = {
            "Account": ["Name", "Type", "Industry", "Rating", "Phone", "Website"],
            "Contact": ["FirstName", "LastName", "Email", "Phone", "Title", "Department"],
            "Opportunity": ["Name", "StageName", "CloseDate", "Amount", "Probability"],
            "Case": ["Subject", "Status", "Priority", "Origin", "Reason", "Description"],
            "Custom": ["Name", "Description", "Status", "Type", "Category", "Value"]
        }

    def generate_field(self, name: str, object_name: str) -> Dict[str, Any]:
        """Generate a single field definition."""
        field_type = random.choice(self.field_types)
        field = {
            "name": name,
            "label": " ".join(word.capitalize() for word in name.split("_")),
            "type": field_type,
            "required": random.choice([True, False]),
            "description": f"Description for {name} field on {object_name}",
            "inlineHelpText": f"Help text for {name} field"
        }
        
        # Add type-specific properties
        if field_type == "Text":
            field["length"] = random.choice([80, 100, 255])
        elif field_type == "LongTextArea":
            field["length"] = random.choice([1000, 2000, 5000])
            field["visibleLines"] = random.choice([3, 5, 10])
        elif field_type == "Number":
            field["precision"] = random.randint(1, 18)
            field["scale"] = random.randint(0, min(field["precision"] - 1, 5))
        elif field_type in ["Picklist", "MultiselectPicklist"]:
            field["values"] = random.choice(self.picklist_values)
            field["defaultValue"] = field["values"][0] if field_type == "Picklist" else None
        
        return field
    
    def generate_object(self, name: str, num_fields: int = 10) -> Dict[str, Any]:
        """Generate a custom object definition."""
        # Basic object properties
        obj = {
            "name": name,
            "label": " ".join(word.capitalize() for word in name.split("_")),
            "pluralLabel": " ".join(word.capitalize() for word in name.split("_")) + "s",
            "description": f"Custom object for {name}",
            "sharingModel": random.choice(["ReadWrite", "Private", "Read"]),
            "enableActivities": random.choice([True, False]),
            "enableReports": True,
            "fields": []
        }
        
        # Determine field templates to use
        template_type = "Custom"
        if name.endswith("__c"):
            base_name = name[:-3]
            if base_name in self.common_field_templates:
                template_type = base_name
        
        # Generate fields
        field_templates = self.common_field_templates[template_type]
        for i in range(num_fields):
            if i < len(field_templates):
                field_name = f"{field_templates[i]}__c"
            else:
                field_name = f"Custom_Field_{i+1}__c"
            
            obj["fields"].append(self.generate_field(field_name, name))
            
        return obj
    
    def generate_workflow_rule(self, object_name: str) -> Dict[str, Any]:
        """Generate a workflow rule for an object."""
        rule_name = f"{object_name}_Update_Rule"
        return {
            "name": rule_name,
            "label": f"Update {object_name} Rule",
            "object": object_name,
            "triggerType": random.choice(["onCreateOrTriggeringUpdate", "onCreateOnly", "onAllChanges"]),
            "active": True,
            "criteriaItems": [
                {
                    "field": f"{object_name}.Custom_Field_1__c",
                    "operation": "equals",
                    "value": "High"
                }
            ],
            "actions": [
                {
                    "type": "FieldUpdate",
                    "name": f"Update_{object_name}_Status",
                    "field": f"{object_name}.Status__c",
                    "value": "Active"
                }
            ]
        }
    
    def generate_schema(self, complexity: str = "medium") -> Dict[str, Any]:
        """Generate a complete schema with custom objects, fields, and workflows."""
        # Determine scope based on complexity
        if complexity == "simple":
            num_objects = 1
            fields_per_object = 5
            include_workflows = False
        elif complexity == "medium":
            num_objects = 3
            fields_per_object = 10
            include_workflows = True
        else:  # complex
            num_objects = 5
            fields_per_object = 15
            include_workflows = True
        
        # Generate the schema
        schema = {
            "apiVersion": "54.0",
            "deploymentName": f"Test_{complexity.capitalize()}_Deployment_{str(uuid.uuid4())[:8]}",
            "objects": {},
            "workflowRules": {}
        }
        
        # Add objects
        for i in range(num_objects):
            obj_name = f"Test_Object_{i+1}__c"
            obj_data = self.generate_object(obj_name, fields_per_object)
            
            # Convert object format to match expected schema structure
            schema["objects"][obj_name] = {
                "label": obj_data["label"],
                "pluralLabel": obj_data["pluralLabel"],
                "description": obj_data["description"],
                "sharingModel": obj_data["sharingModel"],
                "enableActivities": obj_data["enableActivities"],
                "enableReports": obj_data["enableReports"],
                "fields": obj_data["fields"]
            }
        
        # Add workflows if needed
        if include_workflows:
            for obj_name in schema["objects"]:
                workflow = self.generate_workflow_rule(obj_name)
                schema["workflowRules"][workflow["name"]] = {
                    "label": workflow["label"],
                    "object": workflow["object"],
                    "triggerType": workflow["triggerType"],
                    "active": workflow["active"],
                    "criteriaItems": workflow["criteriaItems"],
                    "actions": workflow["actions"]
                }
        
        return schema
    
    def save_schema(self, schema: Dict[str, Any], filename: str) -> str:
        """Save the schema to a file and return the file path."""
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, 'w') as f:
            json.dump(schema, f, indent=2)
        return file_path
    
    def generate_test_suite(self) -> Dict[str, str]:
        """Generate a suite of test schemas with different complexities."""
        schemas = {}
        
        for complexity in ["simple", "medium", "complex"]:
            schema = self.generate_schema(complexity)
            filename = f"{complexity}_schema.json"
            file_path = self.save_schema(schema, filename)
            schemas[complexity] = file_path
            
        # Generate an edge case schema with special characters and extreme values
        edge_schema = self.generate_schema("medium")
        
        # Add some edge cases - adjust this to match your schema format
        test_object = list(edge_schema["objects"].keys())[0]
        edge_schema["objects"][test_object]["fields"].append({
            "name": "Field_With_Special_Ch@r$__c",
            "label": "Field With Special Ch@r$",
            "type": "Text",
            "length": 32767,  # Maximum length
            "required": True
        })
        
        file_path = self.save_schema(edge_schema, "edge_case_schema.json")
        schemas["edge"] = file_path
        
        return schemas

if __name__ == "__main__":
    generator = TestDataGenerator()
    schemas = generator.generate_test_suite()
    
    print("Generated the following test schemas:")
    for complexity, file_path in schemas.items():
        print(f"- {complexity.capitalize()}: {file_path}")