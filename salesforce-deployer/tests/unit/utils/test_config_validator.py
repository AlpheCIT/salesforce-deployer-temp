import unittest
import json
import tempfile
import os

from src.utils.config_validator import validate_config


class TestConfigValidator(unittest.TestCase):
    
    def setUp(self):
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_validate_valid_config(self):
        """Test validation of a valid configuration."""
        # Create a valid configuration
        valid_config = {
            "objects": {
                "Test_Object__c": {
                    "label": "Test Object",
                    "fields": [
                        {"name": "Test_Field__c", "type": "Text", "length": 255}
                    ]
                }
            },
            "workflowRules": {
                "Test_Rule": {
                    "description": "Test Rule",
                    "criteria": "Test_Object__c.Test_Field__c = 'Value'",
                    "actions": [
                        {"type": "Email Alert", "field": "Owner.Email"}
                    ]
                }
            }
        }
        
        # Validate the configuration
        result = validate_config(valid_config)
        
        # Should be valid
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)
    
    def test_validate_invalid_config(self):
        """Test validation of an invalid configuration."""
        # Create an invalid configuration (missing required fields)
        invalid_config = {
            "objects": {
                "Test_Object__c": {
                    # Missing label
                    "fields": [
                        # Missing name
                        {"type": "Text", "length": 255}
                    ]
                }
            },
            "workflowRules": {
                "Test_Rule": {
                    # Missing criteria
                    "actions": [
                        # Missing type
                        {"field": "Owner.Email"}
                    ]
                }
            }
        }
        
        # Validate the configuration
        result = validate_config(invalid_config)
        
        # Should be invalid
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["errors"]), 0)
    
    def test_validate_unknown_field_type(self):
        """Test validation with unknown field type."""
        # Create a configuration with unknown field type
        config = {
            "objects": {
                "Test_Object__c": {
                    "label": "Test Object",
                    "fields": [
                        {"name": "Test_Field__c", "type": "UnknownType"}
                    ]
                }
            }
        }
        
        # Validate the configuration
        result = validate_config(config)
        
        # Should be invalid due to unknown field type
        self.assertFalse(result["valid"])
        self.assertTrue(any("unknown field type" in e.lower() for e in result["errors"]))
    
    def test_validate_missing_reference(self):
        """Test validation with missing lookup reference."""
        # Create a configuration with a lookup field missing reference
        config = {
            "objects": {
                "Test_Object__c": {
                    "label": "Test Object",
                    "fields": [
                        {"name": "Lookup_Field__c", "type": "Lookup"}
                        # Missing referenceTo
                    ]
                }
            }
        }
        
        # Validate the configuration
        result = validate_config(config)
        
        # Should be invalid due to missing reference
        self.assertFalse(result["valid"])
        self.assertTrue(any("referenceto" in e.lower() for e in result["errors"]))
    
    def test_validate_from_file(self):
        """Test validation from a file."""
        # Create a valid configuration file
        config_file = os.path.join(self.temp_dir, "valid_config.json")
        with open(config_file, 'w') as f:
            json.dump({
                "objects": {
                    "Test_Object__c": {
                        "label": "Test Object",
                        "fields": [
                            {"name": "Test_Field__c", "type": "Text", "length": 255}
                        ]
                    }
                }
            }, f)
        
        # Validate from file
        result = validate_config(config_file=config_file)
        
        # Should be valid
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)


if __name__ == "__main__":
    unittest.main()