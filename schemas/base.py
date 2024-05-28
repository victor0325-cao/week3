import datetime
from typing import List, Any, Dict, Union
from enum import Enum, IntEnum
from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    code: int = 200

class PageRequest(BaseModel):
    page: int = Field(..., ge=1)
    size: int = Field(..., ge=1, le=20)

class WellDocEnum(Enum):

    @classmethod
    def __modify_schema__(cls, schema: Dict[str, Any]):
        schema["enum"] = [f"{choice.name} ({choice.value})" for choice in cls]
        return schema

class WellDocIntEnum(int, Enum):
    @classmethod
    def __modify_schema__(cls, schema: Dict[str, Any]):
        schema["enum"] = [f"{choice.name} ({choice.value})" for choice in cls]
        return schema

class TextReadingEditBody(BaseModel):
    content_id: str
    situation: str = None
    reply: str = None
