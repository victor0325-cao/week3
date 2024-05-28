import uuid
import datetime
import logging
import asyncio
import httpx

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query

from config import config

from schemas.exceptions import ParamInvalid, AuthInvalid, ServerError
from schemas.star import *

from api.auth import verify_secret

from . import utils

router = APIRouter(
    dependencies=[
        Depends(verify_secret),
    ]
)

#用户注册
@router.post("/user/logon")
async def create_user():
    user_entity = await utils.UsersDAL.add()
    return user_entity


#信息修改
@router.put("/user/info")
async def update_user(user_id: int):
    user_entity = await utils.UsersDAL.update_user(user_id)
    return user_entity

#显示顾问列表
@router.get("/user/adviser/list")
async def user_advisor_list():
    advisor_list = await utils.UsersDAL.user_advisor_list()
    return advisor_list

#显示顾问主页
@router.get("/user/advisor/home")
async def user_advisor_home():
    advisor_home = await utils.UsersDAL.user_advisor_home()
    return advisor_home


#收藏顾问
@router.post("/user/save_adviser")
async def save_adviser(user_id: str):
    save  = await utils.UsersDAL.save_adviser(user_id)
    return save


#用户流水
@router.post("/user/coin_flow")
async def user_coin_flow(user_id: int, coin_change: int, description: str):
   user = await utils.UsersDAL.user_coin_flow(user_id, coin_change, description)
   return user




