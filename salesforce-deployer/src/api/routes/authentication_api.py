# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from .authentication_api_base import BaseAuthenticationApi
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
from src.models.authentication_response import AuthenticationResponse
from src.models.error_response import ErrorResponse
from src.models.login_request import LoginRequest
from src.models.o_auth_request import OAuthRequest
from openapi_server.security_api import get_token_BearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/auth/login",
    responses={
        200: {"model": AuthenticationResponse, "description": "Authentication successful"},
        401: {"model": ErrorResponse, "description": "Authentication failed"},
    },
    tags=["authentication"],
    summary="Authenticate with Salesforce credentials",
    response_model_by_alias=True,
)
async def authenticate_with_credentials(
    login_request: LoginRequest = Body(None, description=""),
) -> AuthenticationResponse:
    """Authenticates a user with their Salesforce username, password, and optional security token to obtain an access token for API access."""
    if not BaseAuthenticationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthenticationApi.subclasses[0]().authenticate_with_credentials(login_request)


@router.post(
    "/auth/oauth",
    responses={
        200: {"model": AuthenticationResponse, "description": "Authentication successful"},
        401: {"model": ErrorResponse, "description": "Authentication failed"},
    },
    tags=["authentication"],
    summary="Authenticate using OAuth 2.0",
    response_model_by_alias=True,
)
async def authenticate_with_o_auth(
    o_auth_request: OAuthRequest = Body(None, description=""),
) -> AuthenticationResponse:
    """Authenticates using the OAuth 2.0 protocol, supporting both web server flow (with auth code) and username-password flow for headless integrations."""
    if not BaseAuthenticationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthenticationApi.subclasses[0]().authenticate_with_o_auth(o_auth_request)


@router.post(
    "/auth/refresh",
    responses={
        200: {"model": AuthenticationResponse, "description": "Token refreshed successfully"},
        401: {"model": ErrorResponse, "description": "Invalid or expired refresh token"},
    },
    tags=["authentication"],
    summary="Refresh authentication token",
    response_model_by_alias=True,
)
async def refresh_token(
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> AuthenticationResponse:
    """Obtains a new access token using a valid refresh token when the current token has expired or is about to expire."""
    if not BaseAuthenticationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthenticationApi.subclasses[0]().refresh_token()
