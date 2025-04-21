# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.validation_api_base import BaseValidationApi
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
from src.models.error_response import ErrorResponse
from src.models.schema_validation_request import SchemaValidationRequest
from src.models.schema_validation_response import SchemaValidationResponse
from openapi_server.security_api import get_token_BearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/schemas/validate",
    responses={
        200: {"model": SchemaValidationResponse, "description": "Schema validation completed"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
    },
    tags=["validation"],
    summary="Validate a schema",
    response_model_by_alias=True,
)
async def validate_schema(
    schema_validation_request: SchemaValidationRequest = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> SchemaValidationResponse:
    """Analyzes a schema for validity, checking component dependencies, references, and compatibility with target Salesforce organizations."""
    if not BaseValidationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseValidationApi.subclasses[0]().validate_schema(schema_validation_request)
