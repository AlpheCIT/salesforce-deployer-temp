# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import StrictStr
from typing import Any, List
from src.models.error_response import ErrorResponse
from src.models.organization import Organization
from src.models.organization_request import OrganizationRequest
from openapi_server.security_api import get_token_BearerAuth

class BaseOrganizationsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseOrganizationsApi.subclasses = BaseOrganizationsApi.subclasses + (cls,)
    async def add_organization(
        self,
        organization_request: OrganizationRequest,
    ) -> Organization:
        """Registers a new Salesforce organization with the system, including connection credentials and organization metadata."""
        ...


    async def delete_organization(
        self,
        orgId: StrictStr,
    ) -> None:
        """Removes a Salesforce organization from the system, including all stored credentials and connection information."""
        ...


    async def get_organization_by_id(
        self,
        orgId: StrictStr,
    ) -> Organization:
        """Retrieves detailed information about a specific Salesforce organization, including its connection status and metadata."""
        ...


    async def get_organizations(
        self,
    ) -> List[Organization]:
        """Retrieves all Salesforce organizations that have been configured for schema extraction and deployment operations."""
        ...


    async def update_organization(
        self,
        orgId: StrictStr,
        organization_request: OrganizationRequest,
    ) -> Organization:
        """Updates the configuration, credentials, or metadata for an existing Salesforce organization connection."""
        ...
