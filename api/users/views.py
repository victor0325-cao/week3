import uuid
import datetime
import logging
import asyncio
import httpx

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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

#@router.post("/user/login_token/")
#async def login(phone_number: str,password: str,login_form: OAuth2PasswordRequestForm = Depends()):
#    message = {
#        phone_number:phone_number,
#        password:password,
#        }
#    try:
#        await utils.UserFormDAL.post_token(message)
#        token_expires = datetime.now(timezone.utc) + timedelta(minutes = 30)
#        token_data = {
#            "phone_number": login_form.username,
#            "exp": token_expires
#            }
#        token = jwt.encode(token_data, SECRET_KEY, ALGORITHMS)
#        return Token(access_token = token, token_type = "bearer")


#信息修改
@router.put("/info")
async def update_user(user_id: int, user: UserBase):
    return await utils.UserDAL.update_user(user_id, user.dict())



#显示顾问列表
@router.get("/adviser/list")
async def user_advisor_list():
    return await utils.UserAdvisorFormDAL.user_advisor_list()



#显示顾问主页
@router.get("/advisor/home")
async def user_advisor_home(advisor_id: str):
    return await utils.UserAdvisorFormDAL.user_advisor_home(advisor_id)
     


#收藏顾问
@router.post("/advisor/save")
async def save_adviser(user_id: str, adviser_id: str):
    user_save = { 
        'user_id': user_id,
        'adviser_id': adviser_id
    }
    return await utils.UseraveDAL.save_advisor(user_save)


#用户流水
@router.post("/coins")
async def user_coin_flow(user_id: int, coin_change: int, description: str):
    current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    coin_flow ={
        'user_id': user_id,
        'coin_change': coin_change,
        'description': description,
        'timestamp': current_timestamp
    }
    user = await utils.CoinFlowDAL.user_coins(coin_flow)
    return user
