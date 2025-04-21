# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import StrictStr
from typing import Any

# Fix imports to use the correct model paths
from src.models.error_response import ErrorResponse
from src.models.schema import Schema as ModelSchema  # Rename if needed
from src.models.schema_comparison_request import SchemaComparisonRequest
from src.models.schema_comparison_response import SchemaComparisonResponse
from src.models.schema_extraction_request import SchemaExtractionRequest
from src.models.schema_extraction_response import SchemaExtractionResponse

# Fix security import
from src.api.routes.security_api import get_token_BearerAuth

class BaseSchemasApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseSchemasApi.subclasses = BaseSchemasApi.subclasses + (cls,)
    
    async def compare_schemas(
        self,
        schema_comparison_request: SchemaComparisonRequest,
    ) -> SchemaComparisonResponse:
        """Performs a detailed comparison between two schemas, identifying added, modified, and removed components with field-level change tracking."""
        ...


    async def delete_schema(
        self,
        schemaId: StrictStr,
    ) -> None:
        """Permanently removes a schema definition and all its associated metadata components from the system."""
        ...


    async def extract_schema(
        self,
        schema_extraction_request: SchemaExtractionRequest,
    ) -> SchemaExtractionResponse:
        """Extracts metadata schema components from a specified Salesforce organization, with options to filter by component types and include standard or managed components."""
        ...


    async def get_schema(
        self,
        schemaId: StrictStr,
    ) -> ModelSchema:
        """Retrieves the complete metadata schema definition by its unique identifier, including all component definitions and relationships."""
        ...


    async def update_schema(
        self,
        schemaId: StrictStr,
        model_schema: ModelSchema,
    ) -> ModelSchema:
        """Updates an existing schema definition with new metadata components, properties, or relationships while preserving its identifier."""
        ...
