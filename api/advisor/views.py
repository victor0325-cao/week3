import uuid
import datetime
import logging
import asyncio
import httpx

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query

from config import config

from schemas.exceptions import ParamInvalid, AuthInvalid, ServerError
from schemas.advisor import *

from api.auth import verify_secret
from schemas.order import AdviserOrderBase

from . import utils

router = APIRouter(
    dependencies=[
        Depends(verify_secret),
    ]
)


#顾问注册
@router.post("/logon", response_model=BaseResponse)
async def create_adviser(create: AdvisorFormBase):
    await utils.AdvisorlogonDAL.add(create.dict())
    return BaseResponse()


#修改信息
@router.put("/info")
async def update_advisor(advisor_id: int, advisor: AdvisorBase):
    advisor = await utils.InfoUpdateDAL.update_advisor(advisor_id, advisor.dict())
    return {"data": advisor}


#显示信息
@router.get("/home")
async def advisor_home():
   return await utils.AdvisorHomeDAL.advisor_home()



#顾问接单状态更新
@router.patch("/home")
async def update_advisor(advisor_id: int, advisor: AdviserOrderBase):
    advisor_entity = await utils.TakeOrderUpdateDAL.update_advisor(advisor_id, advisor.dict())
    return advisor_entity


#顾问服务状态打开，关闭，金额调整
@router.post("/home/service_settings")
async def update_service(advisor_id: int, service: AdvisorServiceBase):
    service = await utils.ServiceUpdateDAL.update_service(advisor_id, service.dict())
    return {"data": service}


#回复用户
@router.post("/reply_user")
async def reply_user(adviser_id: int, order_id: str, reply: AdvisorReplyBase):

    new_reply = {
        "adviser_id":adviser_id,
        "order_id":order_id,
        "reply_text":reply.reply_text
    }
    await utils.AdvisorReplyDAL.reply_user(new_reply)


#顾问端：用户金币
@router.post("/user_coin_flow")
async def user_coin_flow(user_id: int, coin_change: int, description: str):
    current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    coin_flow = [{
        'user_id': user_id,
        'coin_change': coin_change,
        'description': description,
        'timestamp': current_timestamp
    }]
    user = await utils.CoinFlowDAL.user_coin_flow(coin_flow[0])
    return user
