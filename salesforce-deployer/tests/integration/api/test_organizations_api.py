# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import StrictStr  # noqa: F401
from typing import Any, List  # noqa: F401
from src.models.error_response import ErrorResponse  # noqa: F401
from src.models.organization import Organization  # noqa: F401
from src.models.organization_request import OrganizationRequest  # noqa: F401


def test_add_organization(client: TestClient):
    """Test case for add_organization

    Add a new Salesforce organization
    """
    organization_request = {"credentials":{"security_token":"ABCDEFGHIJKLMNOP","password":"myPassword123","client_id":"3MVG9e2mBbZnmcolVXiRm8YNot7VI5W_oiqJuBDdDUNF9s45MfoiV2h_nI2paMT1QA_yw3UxQncI7Goz8L1A7","client_secret":"123456789012345678","username":"user@example.com"},"name":"My Production Org","description":"Production Salesforce instance","type":"production","instance_url":"https://na1.salesforce.com"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/organizations",
    #    headers=headers,
    #    json=organization_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_organization(client: TestClient):
    """Test case for delete_organization

    Delete organization
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/organizations/{orgId}".format(orgId='org_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_organization_by_id(client: TestClient):
    """Test case for get_organization_by_id

    Get organization details by ID
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/organizations/{orgId}".format(orgId='org_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_organizations(client: TestClient):
    """Test case for get_organizations

    Get a list of connected Salesforce organizations
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/organizations",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_organization(client: TestClient):
    """Test case for update_organization

    Update organization details
    """
    organization_request = {"credentials":{"security_token":"ABCDEFGHIJKLMNOP","password":"myPassword123","client_id":"3MVG9e2mBbZnmcolVXiRm8YNot7VI5W_oiqJuBDdDUNF9s45MfoiV2h_nI2paMT1QA_yw3UxQncI7Goz8L1A7","client_secret":"123456789012345678","username":"user@example.com"},"name":"My Production Org","description":"Production Salesforce instance","type":"production","instance_url":"https://na1.salesforce.com"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/organizations/{orgId}".format(orgId='org_id_example'),
    #    headers=headers,
    #    json=organization_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

