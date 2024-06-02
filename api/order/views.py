import uuid
import logging
import asyncio
import httpx
import redis

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query
from datetime import datetime, timedelta, timezone
from config import config

from schemas.exceptions import ParamInvalid, AuthInvalid, ServerError
from schemas.order import *

from pyutil.time import time
from pyutil.time.random_number import generate_number
#from pyutil.data.redis import make_redis
from api.auth import verify_secret

from . import utils

router = APIRouter(
    dependencies=[
        Depends(verify_secret),
    ]
)


#订单创建
@router.post("/create")
async def order_create(
    id: int,
    create: UserOrderCreateBase
    ):
    general_situation = create.general_situation
    specific_question = create.specific_question
    attach_picture = create.attach_picture

    order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    delivery_time = (datetime.datetime.now() + datetime.timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')

    new_order = {
        'user_id': id,
        'general_situation': general_situation,
        'specific_question': specific_question,
        'attach_picture': attach_picture,
        'order_id': generate_number(18),
        'order_time': order_time,
        'delivery_time': delivery_time,
        'status': "Pending"
    }
#    await utils.UserDAL.reduce_coins(user_id, 10)
    await asyncio.create_task(time.update_status(order_time))
    await utils.OrderDAL.add(new_order)
    return {"data": new_order}
#订单列表
@router.get("/list")
async def order_list():
    list = await utils.OrderDAL.order_list()
    return list

#订单详情
@router.get("/details")
async def order_details(user_id: int):
    order = await utils.OrderDAL.order_details(user_id)
    return order
#    cache_key = f"user_order_details:{phone_number}"
#    cached_results = redis_cli.get(cache_key)
#     if cached_results:
#         return json.loads(cached_results)
#
#     results = []
#     for user_entity, order_creation in user_details:
#
#         user_dict = {
#             "name": user_entity.name,
#             "status": order_creation.status,
#             "order_time": order_creation.order_time,
#             "Order ID":order_creation.order_id,
#             "general_situation":order_creation.general_situation,
#             "specific_question": order_creation.specific_question
#             }
#         results.append(user_dict)
#     return results





