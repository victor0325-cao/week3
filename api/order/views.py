import uuid
import datetime
import logging
import asyncio
import httpx

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query

from config import config

from schemas.exceptions import ParamInvalid, AuthInvalid, ServerError
from schemas.order import *

from api.auth import verify_secret

from . import utils

router = APIRouter(
    dependencies=[
        Depends(verify_secret),
    ]
)

#订单创建
@router.post("/order/create")
async def order_create(user_id: int, order_create:UserOrderCreateBase):
    await utils.OrderDAl.add()

#订单列表
@router.get("/order/list")
async def order_list():
    await utils.OrderDAL.order_list()
    return order

#订单详情
@router.get("/order/details")
async def order_details():
    await utils.OrderDAL.order_details()
    return order






