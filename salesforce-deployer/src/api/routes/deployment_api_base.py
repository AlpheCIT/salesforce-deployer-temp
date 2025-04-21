# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import StrictStr
from src.models.deployment_request import DeploymentRequest
from src.models.deployment_response import DeploymentResponse
from src.models.deployment_status import DeploymentStatus
from src.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_BearerAuth

class BaseDeploymentApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDeploymentApi.subclasses = BaseDeploymentApi.subclasses + (cls,)
    async def cancel_deployment(
        self,
        deploymentId: StrictStr,
    ) -> DeploymentStatus:
        """Attempts to cancel an in-progress deployment operation, rolling back any changes if possible based on the deployment phase."""
        ...


    async def deploy_schema(
        self,
        deployment_request: DeploymentRequest,
    ) -> DeploymentResponse:
        """Initiates a deployment process to apply schema changes to a target Salesforce organization with configurable validation and rollback options."""
        ...


    async def get_deployment_status(
        self,
        deploymentId: StrictStr,
    ) -> DeploymentStatus:
        """Retrieves the current status, progress, and results of an ongoing or completed deployment operation."""
        ...
