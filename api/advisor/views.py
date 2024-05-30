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

from . import utils

router = APIRouter(
    dependencies=[
        Depends(verify_secret),
    ]
)

#顾问注册
@router.post("/logon",response_model=BaseResponse)
async def create_adviser(create: AdvisorFormBase):
    await utils.AdvisorlogonDAL.add(create)
    return BaseResponse()
    

#修改信息
@router.put("/info")
async def update_advisor(advisor_id: int, advisor:AdvisorBase):
    advisor = await utils.InfoUpdateDAL.update_advisor(advisor_id)
    return { "data": advisor }


#显示信息
@router.get("/home")
async def advisor_home():
   advisor =  await utils.AdvisorHomeDAL.advisor_home()
   return {"data": advisor}

#顾问接单状态更新
@router.patch("/home")
async def update_advisor(advisor_id: int, advisor: AdvisorBase):
    advisor_entity = await utils.TakeOrderUpdateDAL.update_advisor(advisor_id)
    return advisor_entity 


#顾问服务状态打开，关闭，金额调整
@router.post("/home/service_settings")
async def update_service(advisor_id: int, service: AdvisorServiceBase):
    service = await utils.ServiceUpdateDAL.update_service(adviser_id)
    return {"data": service} 

#回复用户
@router.post("/reply_user")
async def reply_user(advisor_id: int, order_id: str, reply: AdvisorReplyBase):
 
    user_order = await utils.ReplyUserDAL.reply_user(advisor_id, order_id)
    return {"data": user_order}

#顾问端：用户金币
@router.post("/user_coin_flow")
async def user_coin_flow(user_id: int,coin_change: int, description: str ):
    user = await utils.UserDal.user_coin_flow(user_id, coin_change, description)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data": user}




