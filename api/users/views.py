import uuid
import datetime
import logging
import asyncio
import httpx

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query
from datetime import datetime

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
async def create_user(create: UserFormBase):
    await utils.UserFormDAL.add(create.dict())
    return BaseResponse


#信息修改
@router.put("/info")
async def update_user(user_id: int, user: UserBase):
    user_entity = await utils.UserDAL.update_user(user_id, user.dict())
    return user_entity


#显示顾问列表
@router.get("/adviser/list")
async def user_advisor_list():
    result = await utils.UserListDAL.user_advisor_list()
    return result


#显示顾问主页
@router.get("/advisor/home/")
async def user_advisor_home(advisor_id: str):
    result = await utils.UserAdvisorHomeDAL.user_advisor_home(advisor_id)
    return result


#收藏顾问
@router.post("/save_adviser")
async def save_adviser(user_id: str, adviser_id: str):
    save = {
        'user_id': user_id,
        'adviser_id': adviser_id
    }
    return await utils.SaveDAL.save_advisor(save)


#用户流水
@router.post("/coin_flow")
async def user_coin_flow(user_id: int, coin_change: int, description: str):
    #    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    coin_flow = [{
        'user_id': user_id,
        'coin_change': coin_change,
        'description': description,
        #  'timestamp': current_timestamp
    }]
    user = await utils.CoinFlowDAL.user_coin_flow(coin_flow[0])
    return user
