# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import StrictStr  # noqa: F401
from src.models.deployment_request import DeploymentRequest  # noqa: F401
from src.models.deployment_response import DeploymentResponse  # noqa: F401
from src.models.deployment_status import DeploymentStatus  # noqa: F401
from src.models.error_response import ErrorResponse  # noqa: F401


def test_cancel_deployment(client: TestClient):
    """Test case for cancel_deployment

    Cancel a deployment
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/deployments/{deploymentId}/cancel".format(deploymentId='deployment_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_deploy_schema(client: TestClient):
    """Test case for deploy_schema

    Deploy schema to a Salesforce organization
    """
    deployment_request = {"schema":{"created_at":"2025-04-21T14:30:00Z","components":{"workflow_rules":{"key":{"criteria":"Account.Status__c = 'Active'","name":"Account_Status_Update","active":1,"description":"Updates Account status based on criteria","actions":[{"field":"Status__c","name":"UpdateAccountStatus","type":"FieldUpdate","value":"Processed"},{"field":"Status__c","name":"UpdateAccountStatus","type":"FieldUpdate","value":"Processed"}],"object":"Account"}},"flows":{"key":{"name":"Lead_Process","description":"Automates lead qualification","label":"Lead Qualification Process","process_type":"AutoLaunchedFlow","trigger_type":"","event_type":"","status":"Active"}},"objects":{"key":{"custom":0,"name":"Account","description":"Standard Account object","name_field":"Name","label":"Account","fields":{"key":{"relationship_name":"","default_value":"Default value","unique":0,"name":"CustomField__c","length":255,"external_id":0,"description":"A custom text field","formula":"","label":"Custom Field","type":"Text","required":0,"reference_to":""}},"sharing_model":"ReadWrite"}},"dashboards":{"key":{"components":[{"report_name":"SalesReport","name":"SalesChart","type":"Chart"},{"report_name":"SalesReport","name":"SalesChart","type":"Chart"}],"name":"Sales_Dashboard","description":"Key sales metrics dashboard","label":"Sales Performance","folder_name":"Sales Dashboards"}}},"api_version":"56.0","source_org_id":"123e4567-e89b-12d3-a456-426614174000","name":"Production Schema April 2025","description":"Current production schema as of April 2025","id":"123e4567-e89b-12d3-a456-426614174000","updated_at":"2025-04-21T14:30:00Z"},"components":["Account.CustomField__c","Account.CustomField__c"],"target_org_id":"223e4567-e89b-12d3-a456-426614174000","schema_id":"123e4567-e89b-12d3-a456-426614174000","options":{"test_level":"NoTestRun","ignore_warnings":0,"run_tests":0,"rollback_on_error":1,"auto_update_package":0,"purge_on_delete":0,"check_only":0}}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/deployments",
    #    headers=headers,
    #    json=deployment_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_deployment_status(client: TestClient):
    """Test case for get_deployment_status

    Get deployment status by ID
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/deployments/{deploymentId}".format(deploymentId='deployment_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

