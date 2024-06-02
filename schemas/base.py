import datetime
from typing import List, Any, Dict, Union
from enum import Enum, IntEnum
from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    code: int = 200


