# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from src.models.authentication_response import AuthenticationResponse
from src.models.error_response import ErrorResponse
from src.models.login_request import LoginRequest
from src.models.o_auth_request import OAuthRequest
from openapi_server.security_api import get_token_BearerAuth

class BaseAuthenticationApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAuthenticationApi.subclasses = BaseAuthenticationApi.subclasses + (cls,)
    async def authenticate_with_credentials(
        self,
        login_request: LoginRequest,
    ) -> AuthenticationResponse:
        """Authenticates a user with their Salesforce username, password, and optional security token to obtain an access token for API access."""
        ...


    async def authenticate_with_o_auth(
        self,
        o_auth_request: OAuthRequest,
    ) -> AuthenticationResponse:
        """Authenticates using the OAuth 2.0 protocol, supporting both web server flow (with auth code) and username-password flow for headless integrations."""
        ...


    async def refresh_token(
        self,
    ) -> AuthenticationResponse:
        """Obtains a new access token using a valid refresh token when the current token has expired or is about to expire."""
        ...
