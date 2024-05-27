import datetime
from enum import IntEnum
from pydantic import BaseModel, Json
from .base import BaseResponse, PageRequest

class UserOrderCreateBase(BaseModel):
    general_situation: str
    specific_question: str
    attach_picture: str     #存照片之后改#

class UserOrderRewardBase(BaseModel):
    rating: str
    write_review: str
    reward: int

class AdviserOrderBase(BaseModel):
    order_status: str
