import datetime
from enum import IntEnum
from pydantic import BaseModel, Json
from .base import BaseResponse, PageRequest


#注册表单
class User_FormBase(BaseModel):
    phone_number: str
    password: str

#更改用户数据
class UserBase(BaseModel):
    name: str         #姓名
    birth: str        #生日
    gender: str       #性别
    bio: str          #简历
    about: str        #介绍
    coin: str         #硬币
