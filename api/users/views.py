import uuid
import datetime
import logging
import asyncio
import httpx

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query

from config import config

from schemas.exceptions import ParamInvalid, AuthInvalid, ServerError
from schemas.users import *

from api.auth import verify_secret

from . import utils

router = APIRouter(
    dependencies=[
        Depends(verify_secret),
    ]
)

#用户注册
@router.post("/logon", response_model=BaseResponse)
async def create_user(create:UserFormBase):
    user_entity = await utils.UserFormDAL.add(create)
    return BaseResponse

#信息修改
@router.put("/info")
async def update_user(user_id: int, user:UserBase):
    user_entity = await utils.UserDAL.update_user(user_id)
    return user_entity

#显示顾问列表
@router.get("/adviser/list")
async def user_advisor_list():
    advisor_list = await utils.UserListDAL.user_advisor_list()
    return advisor_list

#显示顾问主页
@router.get("/advisor/home")
async def user_advisor_home():
    advisor_home = await utils.UserAdvisorHomeDAL.user_advisor_home()
    return advisor_home


#收藏顾问
@router.post("/save_adviser")
async def save_adviser(user_id: str):
    save  = await utils.SaveDAL.save_adviser(user_id)
    return save


#用户流水
@router.post("/coin_flow")
async def user_coin_flow(user_id: int, coin_change: int, description: str):
   user = await utils.CoinFlowDAL.user_coin_flow(user_id, coin_change, description)
   return user



