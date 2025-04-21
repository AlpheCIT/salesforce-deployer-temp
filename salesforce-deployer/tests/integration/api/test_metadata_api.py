# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from src.models.error_response import ErrorResponse  # noqa: F401
from src.models.field_metadata import FieldMetadata  # noqa: F401
from src.models.object_metadata import ObjectMetadata  # noqa: F401


def test_get_object_by_name(client: TestClient):
    """Test case for get_object_by_name

    Get object details by name
    """
    params = [("schema_id", 'schema_id_example')]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/metadata/objects/{objectName}".format(objectName='object_name_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_object_fields(client: TestClient):
    """Test case for get_object_fields

    Get fields for an object
    """
    params = [("schema_id", 'schema_id_example')]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/metadata/objects/{objectName}/fields".format(objectName='object_name_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_objects(client: TestClient):
    """Test case for get_objects

    Get a list of objects
    """
    params = [("schema_id", 'schema_id_example')]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/metadata/objects",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

