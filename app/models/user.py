# app/models/user.py
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, GetJsonSchemaHandler, GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core.core_schema import ValidationInfo
from typing import Any

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        from pydantic_core import core_schema

        def validate(value: Any, info: ValidationInfo) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)

        return core_schema.general_plain_validator_function(validate)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string", "format": "objectid"}

    def __str__(self):
        return str(self)


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    api_key: str
    api_token: str
    balance: float = 0.0
    is_active: bool = True
    is_admin: bool = False

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
    )

class UserCreateModel(BaseModel):
    username: str

class UserPublicModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    balance: float = 0.0
    is_active: bool = True
    is_admin: bool = False

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
    )

class ImageModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    image_url: str

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
    )
