# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.metadata_api_base import BaseMetadataApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from src.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictStr
from typing import List, Optional
from typing_extensions import Annotated
from src.models.error_response import ErrorResponse
from src.models.field_metadata import FieldMetadata
from src.models.object_metadata import ObjectMetadata
from openapi_server.security_api import get_token_BearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/metadata/objects/{objectName}",
    responses={
        200: {"model": ObjectMetadata, "description": "Object details retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Object not found"},
    },
    tags=["metadata"],
    summary="Get object details by name",
    response_model_by_alias=True,
)
async def get_object_by_name(
    objectName: StrictStr = Path(..., description=""),
    schema_id: Annotated[Optional[StrictStr], Field(description="ID of the schema to get the object from. If not provided, the object from the connected Salesforce org will be returned.")] = Query(None, description="ID of the schema to get the object from. If not provided, the object from the connected Salesforce org will be returned.", alias="schemaId"),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> ObjectMetadata:
    """Fetches comprehensive metadata for a specific object, including its fields, relationships, and configuration properties."""
    if not BaseMetadataApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMetadataApi.subclasses[0]().get_object_by_name(objectName, schema_id)


@router.get(
    "/metadata/objects/{objectName}/fields",
    responses={
        200: {"model": List[FieldMetadata], "description": "Fields retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Object not found"},
    },
    tags=["metadata"],
    summary="Get fields for an object",
    response_model_by_alias=True,
)
async def get_object_fields(
    objectName: StrictStr = Path(..., description=""),
    schema_id: Annotated[Optional[StrictStr], Field(description="ID of the schema to get fields from. If not provided, fields from the connected Salesforce org will be returned.")] = Query(None, description="ID of the schema to get fields from. If not provided, fields from the connected Salesforce org will be returned.", alias="schemaId"),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> List[FieldMetadata]:
    """Returns a list of all fields defined for a specific object, with their data types, validation rules, and relationships."""
    if not BaseMetadataApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMetadataApi.subclasses[0]().get_object_fields(objectName, schema_id)


@router.get(
    "/metadata/objects",
    responses={
        200: {"model": List[ObjectMetadata], "description": "List of objects retrieved successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
    tags=["metadata"],
    summary="Get a list of objects",
    response_model_by_alias=True,
)
async def get_objects(
    schema_id: Annotated[Optional[StrictStr], Field(description="ID of the schema to get objects from. If not provided, objects from the connected Salesforce org will be returned.")] = Query(None, description="ID of the schema to get objects from. If not provided, objects from the connected Salesforce org will be returned.", alias="schemaId"),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> List[ObjectMetadata]:
    """Retrieves a list of all available objects from either a stored schema or directly from a connected Salesforce organization."""
    if not BaseMetadataApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMetadataApi.subclasses[0]().get_objects(schema_id)
