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
    await utils.AdvisorDAL.add(create)
    return BaseResponse()
    
#     adviser_entity = Adviser_FormEntity(
#        phone_number = adviser.phone_number,
#        password = adviser.password
#        )
#    session.add(adviser_entity)
#    session.commit()
#    return adviser_entity

#修改信息
@router.put("/info")
async def update_advisor(advisor_id: int, advisor:AdvisorBase):
    advisor = await utils.AdvisorDAL.update_advisor(advisor_id)
    return { "data": advisor }

#    adviser_entity = session.query(AdviserEntity).filter(AdviserEntity.id == adviser_id).first()
#    if adviser_entity:
#
#        adviser_entity.name = adviser.name
#        adviser_entity.bio = adviser.bio
#        adviser_entity.work = adviser.work
#        adviser_entity.about = adviser.about

#
#        try:
#            session.commit()
#            session.refresh(adviser_entity)
#             return AdviserOut(id=adviser_entity.id, message="User updated successfully")
#        except sqlalchemy.exc.IntegrityError as e:
#             raise HTTPException(status_code=400, detail="Error updating user: " + str(e))
#        else:
#             raise HTTPException(status_code=404 , detail="User not found")


#显示信息
@router.get("/home")
async def advisor_home():
   advisor =  await utils.AdvisorHomeDAL.advisor_home()
   return {"data": advisor}

#顾问接单状态更新
@router.patch("/home")
async def update_advisor(advisor_id: int, advisor: AdvisorBase):
    advisor_entity = await utils.AdvisorDAL.update_advisor(advisor_id)
    return advisor_entity

#    adviser_entity = session.query(AdviserOrderStatus).filter(AdviserOrderStatus.id == adviser_id).first()
#
#    if adviser_entity:
#        adviser_entity.order_status = adviser.order_status
#        try:
#            session.commit()
#            session.refresh(adviser_entity)
#            return AdviserOut(id=adviser_entity.id, message="User updated successfully")
#        except sqlalchemy.exc.IntegrityError as e:
#            raise HTTPException(status_code=400, detail="Error updating user: " + str(e))
#        else:
#            raise HTTPException(status_code=404, detail="User not found")

#顾问服务状态打开，关闭，金额调整
@router.post("/home/service_settings")
async def update_service(advisor_id: int, service: AdvisorServiceBase):
    service = await utils.AdvisorDal.update_service(adviser_id)
    return {"data": service}

#    adviser_service = session.query(AdviserServiceSettings).filter(AdviserServiceSettings.id == adviser_id).first()
#
#    if adviser_service:
#        adviser_service.service_adjustment = adviser.service_adjustment
#        if adviser.service_adjustment == 'open':
#            adviser_service.amount_adjustment = adviser.amount_adjustment
#
#        try:
#            session.commit()
#            session.refresh(adviser_service)
#            return AdviserOut(id=adviser_service.id, message="User updated successfull    y")
#        except sqlalchemy.exc.IntegrityError as e:
#            raise HTTPException(status_code=400, detail="Error updating user: " + str(    e))
#        else:
#             raise HTTPException(status_code=404, detail="User not found")
#
#回复用户
@router.post("/reply_user")
async def reply_user(advisor_id: int, order_id: str, reply: AdvisorReplyBase):
 
    user_order = await utils.AdvisorDAL.reply_user(advisor_id, order_id)
    return {"data": user_order}

#     user_order = session.query(UserOrderCreation).filter(UserOrderCreation.id == order_id).first()
#
#    if not user_order:
#        raise HTTPException(status_code=404, detail="Order not found")
#
#    reply_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#    delivery_time = reply_time
#
#    new_reply = AdviserReply(
#         adviser_id = adviser_id,
#        order_id = order_id,
#        reply_text = adviser_reply.reply_text
#        )
#    adviser = session.query(AdviserHomeEntity).get(adviser_id)
##这里对顾问回复获得金币未做限制，同一个顾问，同一个订单多次回复，多次增加
#    if adviser:
#        adviser.coin += 10
#
#    if user_order:
#         user_order.status = "Completed"
#        user_order.delivery_time = reply_time
#
#    session.add(new_reply)
#    session.commit()
#
#    return {
#         "Adviser Name": adviser.name,
#        "status": user_order.status,
#        "Order Time": user_order.order_time,
#        "Delivery Time": reply_time,
#        "Order ID": order_id,
#        "Request Details":{
#             "Name": user_order.user_data.name,
#            "Date of Birth": user_order.user_data.birth,
#            "Gender": user_order.user_data.gender,
#            "General Situation": user_order.general_situation,
#            "Specific Question": user_order.specific_question,
#            "Reply":new_reply.reply_text
#             }
#        }
#
#顾问端：用户金币
@router.post("/user_coin_flow")
async def user_coin_flow(user_id: int,coin_change: int, description: str ):
    user = await utils.UserDal.user_coin_flow(user_id, coin_change, description)
    return {"data": user}

#    u ser = session.query(UserEntity).get(user_id)
#
#    if not user:
#        raise HTTPException(status_code=404, detail="User not found")
#
#    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#    user.coin += coin_change
#
#    coin_flow = UserCoinFlow(
#        user_id = user.id,
#        coin_change = coin_change,
#        description = description,
#        timestamp = current_timestamp
#         )
#
#    session.add(coin_flow)
#    session.commit()
#
#    coin_flows = session.query(UserCoinFlow).all()
#
#    coin_flow = [{
#        "id": flow.id,
#        "user_id": flow.user_id,
#        "coin_change": flow.coin_change,
#        "description": flow.description,
#        "timestamp": flow.timestamp.strftime('%Y-%m-%d %H:%M:%S')
#        }for flow in coin_flows
#         ]
#
#    return {"coin_flows": coin_flows}



