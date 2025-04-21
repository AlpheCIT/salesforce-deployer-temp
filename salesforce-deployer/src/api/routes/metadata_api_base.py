# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import List, Optional
from typing_extensions import Annotated
from src.models.error_response import ErrorResponse
from src.models.field_metadata import FieldMetadata
from src.models.object_metadata import ObjectMetadata
from openapi_server.security_api import get_token_BearerAuth

class BaseMetadataApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseMetadataApi.subclasses = BaseMetadataApi.subclasses + (cls,)
    async def get_object_by_name(
        self,
        objectName: StrictStr,
        schema_id: Annotated[Optional[StrictStr], Field(description="ID of the schema to get the object from. If not provided, the object from the connected Salesforce org will be returned.")],
    ) -> ObjectMetadata:
        """Fetches comprehensive metadata for a specific object, including its fields, relationships, and configuration properties."""
        ...


    async def get_object_fields(
        self,
        objectName: StrictStr,
        schema_id: Annotated[Optional[StrictStr], Field(description="ID of the schema to get fields from. If not provided, fields from the connected Salesforce org will be returned.")],
    ) -> List[FieldMetadata]:
        """Returns a list of all fields defined for a specific object, with their data types, validation rules, and relationships."""
        ...


    async def get_objects(
        self,
        schema_id: Annotated[Optional[StrictStr], Field(description="ID of the schema to get objects from. If not provided, objects from the connected Salesforce org will be returned.")],
    ) -> List[ObjectMetadata]:
        """Retrieves a list of all available objects from either a stored schema or directly from a connected Salesforce organization."""
        ...
