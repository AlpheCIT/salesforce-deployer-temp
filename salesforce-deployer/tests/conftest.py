"""
Shared test fixtures for Salesforce Schema Deployer tests.

This file contains pytest fixtures that can be used across multiple test files.
Fixtures defined here are automatically available to all test files without explicit import.
"""
import os
import sys

# Add the project root directory to Python's module search path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to sys.path")

# Your existing imports and fixtures below...
import json
import tempfile
import shutil
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files that is cleaned up after the test."""
    dir_path = tempfile.mkdtemp()
    yield dir_path
    shutil.rmtree(dir_path)


@pytest.fixture
def sample_config():
    """Return a sample configuration dictionary for testing."""
    return {
        "objects": {
            "Test_Object__c": {
                "label": "Test Object",
                "fields": [
                    {"name": "Text_Field__c", "type": "Text", "length": 255},
                    {"name": "Picklist_Field__c", "type": "Picklist", "values": ["Option1", "Option2"]},
                    {"name": "Lookup_Field__c", "type": "Lookup", "referenceTo": "Account"}
                ]
            },
            "Related_Object__c": {
                "label": "Related Object",
                "fields": [
                    {"name": "Name", "type": "Text", "length": 255},
                    {"name": "Parent__c", "type": "Lookup", "referenceTo": "Test_Object__c"}
                ]
            }
        },
        "workflowRules": {
            "Test_Object_Status_Change": {
                "description": "Rule to notify when status changes",
                "criteria": "ISCHANGED(Status__c)",
                "actions": [
                    {"type": "Email Alert", "field": "Owner.Email"}
                ]
            }
        },
        "dashboards": {
            "Test_Dashboard": {
                "widgets": [
                    {"type": "Chart", "title": "Test Chart", "source": "Test_Report"}
                ]
            }
        },
        "lightningFlows": {
            "Test_Flow": {
                "description": "Test Flow Description"
            }
        }
    }


@pytest.fixture
def config_file(temp_dir, sample_config):
    """Create a sample configuration file in the temporary directory."""
    config_path = os.path.join(temp_dir, "config.json")
    with open(config_path, 'w') as f:
        json.dump(sample_config, f, indent=2)
    return config_path


@pytest.fixture
def env_file(temp_dir):
    """Create a sample .env file in the temporary directory."""
    env_path = os.path.join(temp_dir, ".env")
    with open(env_path, 'w') as f:
        f.write("SF_USERNAME=test@example.com\n")
        f.write("SF_PASSWORD=password123\n")
        f.write("SF_SECURITY_TOKEN=token123\n")
        f.write("SF_INSTANCE_URL=https://test.salesforce.com\n")
    return env_path


@pytest.fixture
def mock_authenticator():
    """Create a mock Salesforce authenticator."""
    mock = MagicMock()
    mock.authenticate.return_value = True
    mock.access_token = "test_token"
    mock.instance_url = "https://test.salesforce.com"
    return mock


@pytest.fixture
def mock_deployment_manager():
    """Create a mock deployment manager."""
    mock = MagicMock()
    mock.deploy.return_value = True
    return mock


@pytest.fixture
def sample_metadata_files(temp_dir):
    """Create sample metadata files in the temporary directory."""
    # Create directory structure
    objects_dir = os.path.join(temp_dir, "objects")
    workflows_dir = os.path.join(temp_dir, "workflows")
    os.makedirs(objects_dir, exist_ok=True)
    os.makedirs(workflows_dir, exist_ok=True)
    
    # Create a sample object file
    with open(os.path.join(objects_dir, "Test_Object__c.object-meta.xml"), "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Test Object</label>
    <deploymentStatus>Deployed</deploymentStatus>
    <sharingModel>ReadWrite</sharingModel>
</CustomObject>""")
    
    # Create a sample workflow file
    with open(os.path.join(workflows_dir, "Test_Object__c.workflow-meta.xml"), "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<Workflow xmlns="http://soap.sforce.com/2006/04/metadata">
    <rules>
        <fullName>Test_Rule</fullName>
        <active>true</active>
        <formula>ISCHANGED(Name)</formula>
        <triggerType>onAllChanges</triggerType>
    </rules>
</Workflow>""")
    
    return temp_dir


@pytest.fixture
def mock_api_response():
    """Create a mock response for API calls."""
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {
        "access_token": "test_token",
        "instance_url": "https://test.salesforce.com"
    }
    return mock


@pytest.fixture
def mock_cli_args():
    """Create mock command-line arguments."""
    class Args:
        config = "config.json"
        env = ".env"
        output = "output_dir"
        verbose = True
        no_deploy = False
        validate = False
    
    return Args()


@pytest.fixture
def problematic_metadata(temp_dir):
    """Create metadata files with common problems for self-healing tests."""
    # Create directory structure
    objects_dir = os.path.join(temp_dir, "objects")
    os.makedirs(objects_dir, exist_ok=True)
    
    # Create object file missing required label
    with open(os.path.join(objects_dir, "Missing_Label__c.object-meta.xml"), "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <deploymentStatus>Deployed</deploymentStatus>
    <sharingModel>ReadWrite</sharingModel>
</CustomObject>""")
    
    # Create object with invalid field reference
    with open(os.path.join(objects_dir, "Invalid_Reference__c.object-meta.xml"), "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Invalid Reference</label>
    <deploymentStatus>Deployed</deploymentStatus>
    <sharingModel>ReadWrite</sharingModel>
    <fields>
        <fullName>BadRef__c</fullName>
        <type>Lookup</type>
        <referenceTo>NonExistent__c</referenceTo>
    </fields>
</CustomObject>""")
    
    return temp_dir


@pytest.fixture
def generated_schemas():
    """Generate and return test schemas for various complexity levels."""
    from tests.utils.generate_test_data import TestDataGenerator
    generator = TestDataGenerator(output_dir=tempfile.mkdtemp())
    return generator.generate_test_suite()


@pytest.fixture(scope="session")
def mock_salesforce_server():
    """Start a mock Salesforce server for integration tests."""
    from tests.utils.mock_salesforce_server import MockSalesforceHandler, MockSalesforceState
    import threading
    from http.server import HTTPServer
    import time
    
    # Create a server in a separate thread
    port = 8123  # Use a specific port for tests
    server_address = ('', port)
    
    # Create shared state
    MockSalesforceHandler.state = MockSalesforceState()
    
    server = HTTPServer(server_address, MockSalesforceHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True  # Thread will exit when the main program exits
    
    # Start the server
    thread.start()
    time.sleep(0.5)  # Give it time to start
    
    # Return server info for the tests to use
    server_info = {
        "url": f"http://localhost:{port}",
        "instance_url": MockSalesforceHandler.state.instance_url,
        "access_token": MockSalesforceHandler.state.access_token
    }
    
    yield server_info
    
    # Cleanup
    server.shutdown()
    thread.join(1)