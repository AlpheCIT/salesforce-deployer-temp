# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.organizations_api_base import BaseOrganizationsApi
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
from typing import Any, List
from src.models.error_response import ErrorResponse
from src.models.organization import Organization
from src.models.organization_request import OrganizationRequest
from openapi_server.security_api import get_token_BearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/organizations",
    responses={
        201: {"model": Organization, "description": "Organization added successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
    },
    tags=["organizations"],
    summary="Add a new Salesforce organization",
    response_model_by_alias=True,
)
async def add_organization(
    organization_request: OrganizationRequest = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> Organization:
    """Registers a new Salesforce organization with the system, including connection credentials and organization metadata."""
    if not BaseOrganizationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseOrganizationsApi.subclasses[0]().add_organization(organization_request)


@router.delete(
    "/organizations/{orgId}",
    responses={
        204: {"description": "Organization deleted successfully"},
        404: {"model": ErrorResponse, "description": "Organization not found"},
    },
    tags=["organizations"],
    summary="Delete organization",
    response_model_by_alias=True,
)
async def delete_organization(
    orgId: StrictStr = Path(..., description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> None:
    """Removes a Salesforce organization from the system, including all stored credentials and connection information."""
    if not BaseOrganizationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseOrganizationsApi.subclasses[0]().delete_organization(orgId)


@router.get(
    "/organizations/{orgId}",
    responses={
        200: {"model": Organization, "description": "Organization details retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Organization not found"},
    },
    tags=["organizations"],
    summary="Get organization details by ID",
    response_model_by_alias=True,
)
async def get_organization_by_id(
    orgId: StrictStr = Path(..., description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> Organization:
    """Retrieves detailed information about a specific Salesforce organization, including its connection status and metadata."""
    if not BaseOrganizationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseOrganizationsApi.subclasses[0]().get_organization_by_id(orgId)


@router.get(
    "/organizations",
    responses={
        200: {"model": List[Organization], "description": "List of organizations retrieved successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
    tags=["organizations"],
    summary="Get a list of connected Salesforce organizations",
    response_model_by_alias=True,
)
async def get_organizations(
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> List[Organization]:
    """Retrieves all Salesforce organizations that have been configured for schema extraction and deployment operations."""
    if not BaseOrganizationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseOrganizationsApi.subclasses[0]().get_organizations()


@router.put(
    "/organizations/{orgId}",
    responses={
        200: {"model": Organization, "description": "Organization updated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Organization not found"},
    },
    tags=["organizations"],
    summary="Update organization details",
    response_model_by_alias=True,
)
async def update_organization(
    orgId: StrictStr = Path(..., description=""),
    organization_request: OrganizationRequest = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> Organization:
    """Updates the configuration, credentials, or metadata for an existing Salesforce organization connection."""
    if not BaseOrganizationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseOrganizationsApi.subclasses[0]().update_organization(orgId, organization_request)
