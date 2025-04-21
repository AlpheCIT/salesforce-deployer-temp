# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.deployment_api_base import BaseDeploymentApi
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
from src.models.deployment_request import DeploymentRequest
from src.models.deployment_response import DeploymentResponse
from src.models.deployment_status import DeploymentStatus
from src.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_BearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/deployments/{deploymentId}/cancel",
    responses={
        200: {"model": DeploymentStatus, "description": "Deployment cancelled successfully"},
        400: {"model": ErrorResponse, "description": "Deployment cannot be cancelled"},
        404: {"model": ErrorResponse, "description": "Deployment not found"},
    },
    tags=["deployment"],
    summary="Cancel a deployment",
    response_model_by_alias=True,
)
async def cancel_deployment(
    deploymentId: StrictStr = Path(..., description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> DeploymentStatus:
    """Attempts to cancel an in-progress deployment operation, rolling back any changes if possible based on the deployment phase."""
    if not BaseDeploymentApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDeploymentApi.subclasses[0]().cancel_deployment(deploymentId)


@router.post(
    "/deployments",
    responses={
        202: {"model": DeploymentResponse, "description": "Deployment started"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
    tags=["deployment"],
    summary="Deploy schema to a Salesforce organization",
    response_model_by_alias=True,
)
async def deploy_schema(
    deployment_request: DeploymentRequest = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> DeploymentResponse:
    """Initiates a deployment process to apply schema changes to a target Salesforce organization with configurable validation and rollback options."""
    if not BaseDeploymentApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDeploymentApi.subclasses[0]().deploy_schema(deployment_request)


@router.get(
    "/deployments/{deploymentId}",
    responses={
        200: {"model": DeploymentStatus, "description": "Deployment status found"},
        404: {"model": ErrorResponse, "description": "Deployment not found"},
    },
    tags=["deployment"],
    summary="Get deployment status by ID",
    response_model_by_alias=True,
)
async def get_deployment_status(
    deploymentId: StrictStr = Path(..., description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> DeploymentStatus:
    """Retrieves the current status, progress, and results of an ongoing or completed deployment operation."""
    if not BaseDeploymentApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDeploymentApi.subclasses[0]().get_deployment_status(deploymentId)
