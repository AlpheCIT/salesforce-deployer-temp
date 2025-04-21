# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import StrictStr  # noqa: F401
from typing import Any  # noqa: F401
from src.models.error_response import ErrorResponse  # noqa: F401
from src.models.model_schema import ModelSchema  # noqa: F401
from src.models.schema_comparison_request import SchemaComparisonRequest  # noqa: F401
from src.models.schema_comparison_response import SchemaComparisonResponse  # noqa: F401
from src.models.schema_extraction_request import SchemaExtractionRequest  # noqa: F401
from src.models.schema_extraction_response import SchemaExtractionResponse  # noqa: F401


def test_compare_schemas(client: TestClient):
    """Test case for compare_schemas

    Compare two schemas
    """
    schema_comparison_request = {"components":["objects","objects"],"source_schema_id":"123e4567-e89b-12d3-a456-426614174000","target_schema_id":"223e4567-e89b-12d3-a456-426614174000"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/schemas/compare",
    #    headers=headers,
    #    json=schema_comparison_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_schema(client: TestClient):
    """Test case for delete_schema

    Delete schema by ID
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/schemas/{schemaId}".format(schemaId='schema_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_extract_schema(client: TestClient):
    """Test case for extract_schema

    Extract schema from a Salesforce organization
    """
    schema_extraction_request = {"include_standard":0,"include_managed":0,"filter":"CustomObject:Account,Contact","components":["objects","objects"],"org_id":"123e4567-e89b-12d3-a456-426614174000"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/schemas/extract",
    #    headers=headers,
    #    json=schema_extraction_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_schema(client: TestClient):
    """Test case for get_schema

    Get schema by ID
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/schemas/{schemaId}".format(schemaId='schema_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_schema(client: TestClient):
    """Test case for update_schema

    Update schema by ID
    """
    model_schema = src.modelschema()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/schemas/{schemaId}".format(schemaId='schema_id_example'),
    #    headers=headers,
    #    json=model_schema,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

