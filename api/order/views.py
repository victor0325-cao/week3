import uuid
import datetime
import logging
import asyncio
import httpx
import redis

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query

from config import config

from schemas.exceptions import ParamInvalid, AuthInvalid, ServerError
from schemas.order import *

from pyutil.time import time

from api.auth import verify_secret

from . import utils

router = APIRouter(
    dependencies=[
        Depends(verify_secret),
    ]
)

redis_client = redis.StrictRedis(host ='0.0.0.0', port=6379, decode_responses=True)

#订单创建
@router.post("/create", response_model=BaseResponse)
async def order_create(user_id: int, create:UserOrderCreateBase):
#    await utils.OrderDAL.add(create)
#    return BaseResponse()

    user = session.query(UserEntity).filter(UserEntity.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not fount")

    order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    delivery = (datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
#添加信息
    new_order = UserOrderCreation(
        user_id = user_id,
        general_situation = order_create.general_situation,
        specific_question = order_create.specific_question,
        attach_picture = order_create.attach_picture,
        order_id = generate_number(18),
        order_time = order_time,
        delivery_time = delivery,
        status = "Pending"
        )
    user.coin -= 10

    # 启动异步定时任务
    asyncio.create_task(time.update_status(order_time))

    session.add(new_order)
    session.commit()

    return {
        "name ": user.name,
        "coin": user.coin,
        "basic information":{
            "name": user.name,
            "birth": user.birth,
            "gender": user.gender
            },
        "general_situation": order_create.general_situation,
        "specific_question": order_create.specific_question,
        "attach_picture": order_create.attach_picture
        }

#订单列表
@router.get("/list")
async def order_list():
#    await utils.OrderDAL.order_list()
#    return order
    user_list = session.query(UserEntity, UserOrderCreation).join(UserOrderCreation).all()
    results = []
    for user_entity, order_creation in user_list:
        user_dict = {
            "name": user_entity.name,
            "order_time": order_creation.order_time,
            "specific_question": order_creation.specific_question,
            "status": order_creation.status
            }
    results.append(user_dict)
    return results

#订单详情
@router.get("/details")
async def order_details():
#    await utils.OrderDAL.order_details()
#    return order
    cache_key = f"user_order_details:{phone_number}"
    cached_results = redis_client.get(cache_key)
    if cached_results:
        return json.loads(cached_results)

    results = []
    for user_entity, order_creation in user_details:

        user_dict = {
            "name": user_entity.name,
            "status": order_creation.status,
            "order_time": order_creation.order_time,
            "Order ID":order_creation.order_id,
            "general_situation":order_creation.general_situation,
            "specific_question": order_creation.specific_question
            }
        results.append(user_dict)
    return results





