# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from src.models.error_response import ErrorResponse
from src.models.schema_validation_request import SchemaValidationRequest
from src.models.schema_validation_response import SchemaValidationResponse
from openapi_server.security_api import get_token_BearerAuth

class BaseValidationApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseValidationApi.subclasses = BaseValidationApi.subclasses + (cls,)
    async def validate_schema(
        self,
        schema_validation_request: SchemaValidationRequest,
    ) -> SchemaValidationResponse:
        """Analyzes a schema for validity, checking component dependencies, references, and compatibility with target Salesforce organizations."""
        ...
