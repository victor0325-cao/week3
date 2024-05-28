import uuid
import datetime
import logging
import asyncio
import httpx

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query

from config import config

from schemas.exceptions import ParamInvalid, AuthInvalid, ServerError
from schemas.alg import *

from api.auth import verify_secret

from . import utils

router = APIRouter(
    dependencies=[
        Depends(verify_secret),
    ]
)

#顾问注册
@router.post("/advisor/logon", response_model=AdvisorFrom)
async def create_adviser(adviser: AdviserForm):
    await utils.AdvisorDAL.add()
    return AdviserForm()

#修改信息
@router.put("/advisor/info", response_model)
async def update_advisor(advisor_id: int, advisor:Advisor):
    advisor_entity = await utils.AdvisorDAL.update_advisor(advisor_id)
    
    if advisor_entity:
        advisor_entity.name = advisor.name
        advisor_entity.bio = advisor.bio
        advisor_entity.work = advisor.work
        advisor_entity.about = advisor.about

    return { "data": advisor_entity }

#显示信息
##之后修改连接只返回一到两条数据##
@router.get("/advisor/home")
async def advisor_home():
   advisor = await utils.AdvisorDAL.advisor_home()
   return {"data": advisor}

#顾问接单状态更新
@router.patch("/advisor/home")
async def update_advisor(advisor_id: int, advisor: AdvisorOrderBase):
    advisor_entity = await utils.AdvisorDAL.update_advisor(advisor_id)
    return advisor_entity

#顾问服务状态打开，关闭，金额调整
@router.post("/advisor/home/service_settings")
async def update_service(advisor_id: int, advisor: AdvisorServiceBase):
    service = await utils.AdvisorDal.update_service(adviser_id)
    return {"data": service}

#回复用户
@router.post("/advisor/reply_user")
async def reply_user(advisor_id: int, order_id: str, advisor_reply: AdvisorReplyBase):
    user_order = await utils.AdvisorDAL.reply_user(advisor_id, order_id)
    return {"data": user_order}

#顾问端：用户金币
@router.post("/advisor/user_coin_flow")
async def user_coin_flow(user_id: int,coin_change: int, description: str ):
    user = await utils.UserDal.user_coin_flow(user_id, coin_change, description)
    return {"data": user}

