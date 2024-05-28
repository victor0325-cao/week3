import datetime
from enum import IntEnum
from pydantic import BaseModel, Json
from .base import BaseResponse, PageRequest


#顾问
class AdviserFormBase(BaseModel):
    phone_number: str
    password: str

class AdviserBase(BaseModel):
    name: str
    bio: str
    work: str
    about: str
    
class AdviserServiceBase(BaseModel):
    id: int
    service_adjustment: str
    amount_adjustment: str

class AdviserReplyBase(BaseModel):
    reply_text: str
