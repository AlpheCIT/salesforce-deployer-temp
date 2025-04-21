# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from .schemas_api_base import BaseSchemasApi
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
from pydantic import StrictStr
from typing import Any
from src.models.error_response import ErrorResponse
from src.models.model_schema import ModelSchema
from src.models.schema_comparison_request import SchemaComparisonRequest
from src.models.schema_comparison_response import SchemaComparisonResponse
from src.models.schema_extraction_request import SchemaExtractionRequest
from src.models.schema_extraction_response import SchemaExtractionResponse
from .security_api import get_token_BearerAuth  # Relative import from same directory

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/schemas/compare",
    responses={
        200: {"model": SchemaComparisonResponse, "description": "Schema comparison completed"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
    },
    tags=["schemas"],
    summary="Compare two schemas",
    response_model_by_alias=True,
)
async def compare_schemas(
    schema_comparison_request: SchemaComparisonRequest = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> SchemaComparisonResponse:
    """Performs a detailed comparison between two schemas, identifying added, modified, and removed components with field-level change tracking."""
    if not BaseSchemasApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSchemasApi.subclasses[0]().compare_schemas(schema_comparison_request)


@router.delete(
    "/schemas/{schemaId}",
    responses={
        204: {"description": "Schema deleted successfully"},
        404: {"model": ErrorResponse, "description": "Schema not found"},
    },
    tags=["schemas"],
    summary="Delete schema by ID",
    response_model_by_alias=True,
)
async def delete_schema(
    schemaId: StrictStr = Path(..., description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> None:
    """Permanently removes a schema definition and all its associated metadata components from the system."""
    if not BaseSchemasApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSchemasApi.subclasses[0]().delete_schema(schemaId)


@router.post(
    "/schemas/extract",
    responses={
        200: {"model": SchemaExtractionResponse, "description": "Schema extraction successful"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
    tags=["schemas"],
    summary="Extract schema from a Salesforce organization",
    response_model_by_alias=True,
)
async def extract_schema(
    schema_extraction_request: SchemaExtractionRequest = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> SchemaExtractionResponse:
    """Extracts metadata schema components from a specified Salesforce organization, with options to filter by component types and include standard or managed components."""
    if not BaseSchemasApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSchemasApi.subclasses[0]().extract_schema(schema_extraction_request)


@router.get(
    "/schemas/{schemaId}",
    responses={
        200: {"model": ModelSchema, "description": "Schema found"},
        404: {"model": ErrorResponse, "description": "Schema not found"},
    },
    tags=["schemas"],
    summary="Get schema by ID",
    response_model_by_alias=True,
)
async def get_schema(
    schemaId: StrictStr = Path(..., description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> ModelSchema:
    """Retrieves the complete metadata schema definition by its unique identifier, including all component definitions and relationships."""
    if not BaseSchemasApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSchemasApi.subclasses[0]().get_schema(schemaId)


@router.put(
    "/schemas/{schemaId}",
    responses={
        200: {"model": ModelSchema, "description": "Schema updated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Schema not found"},
    },
    tags=["schemas"],
    summary="Update schema by ID",
    response_model_by_alias=True,
)
async def update_schema(
    schemaId: StrictStr = Path(..., description=""),
    model_schema: ModelSchema = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> ModelSchema:
    """Updates an existing schema definition with new metadata components, properties, or relationships while preserving its identifier."""
    if not BaseSchemasApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSchemasApi.subclasses[0]().update_schema(schemaId, model_schema)
