import datetime
from enum import IntEnum
from pydantic import BaseModel, Json
from .base import BaseResponse


#顾问
class AdvisorFormBase(BaseModel):
    phone_number: str
    password: str

class AdvisorBase(BaseModel):
    name: str
    bio: str
    work: str
    about: str
    
class AdvisorServiceBase(BaseModel):
    id: int
    service_adjustment: str
    amount_adjustment: str

class AdvisorReplyBase(BaseModel):
    reply_text: str
