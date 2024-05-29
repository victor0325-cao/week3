import uuid
import datetime
import logging
import asyncio
import httpx

from typing import Union, Any
from fastapi import Request, Depends, HTTPException, APIRouter, Query

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
async def create_user(create:UserFormBase):
#    user_entity = await utils.UsersDAL.add(create)
#    return BaseResponse
    user_entity = User_FormEntity(phone_number = user.phone_number, password = user.password)
    session.add(user_entity)
    session.commit()
    return user_entity

#信息修改
@router.put("/info")
async def update_user(user_id: int, user:UserBase):
#    user_entity = await utils.UsersDAL.update_user(user_id)
#    return user_entity
    user_entity = session.query(UserEntity).filter(UserEntity.id == user_id).first()
    if user_entity:
        user_entity.name = user.name
        user_entity.birth = user.birth
        user_entity.gender = user.gender
        user_entity.bio = user.bio
        user_entity.about = user.about
        user_entity.coin = user.coin
        try:
            session.commit()
            session.refresh(user_entity)
            return UserOut(id=user_entity.id, message="User updated successfully")
        except sqlalchemy.exc.IntegrityError as e:
            raise HTTPException(status_code=400, detail="Error updating user: " + str(e))
        else:
             raise HTTPException(status_code=404, detail="User not found")

#显示顾问列表
@router.get("/adviser/list")
async def user_advisor_list():
#    advisor_list = await utils.UsersDAL.user_advisor_list()
#    return advisor_list
    user_adviser = session.query(AdviserEntity).order_by(asc(AdviserEntity.name)).all()
    results = [{
        "name": adviser.name,
        "bio": adviser.bio
        }for adviser in user_adviser
        ] 
    return results 

#显示顾问主页
@router.get("/advisor/home")
async def user_advisor_home():
#    advisor_home = await utils.UsersDAL.user_advisor_home()
#    return advisor_home

    user_adviser = session.query(AdviserEntity,AdviserServiceSettings).join(AdviserServiceSettings).all()
    results = [{
        "name":adviser_Entity.anme,
        "bio":adviser_Entity.bio,
        "Text resding": service_settings.amount_adjustment,
        "About Me": adviser_Entity.about
        }for adviser_Entity, service_settings in user_adviser
        ]
    return results

#收藏顾问
@router.post("/save_adviser")
async def save_adviser(user_id: str):
#    save  = await utils.UsersDAL.save_adviser(user_id)
#    return save

    if not user_collection:
        raise HTTPException(status_code=404, detail="User not found")

    collection = UserCollection(
        user_id = collection_data.user_id,
        adviser_id = collection_data.adviser_id,
        )
    session.add(collection)
    session.commit()

    return{
        "User Name":user_collection.name,
        "Adviser Name": collection.adviser_data.name,
        } 

#用户流水
@router.post("/coin_flow")
async def user_coin_flow(user_id: int, coin_change: int, description: str):
#   user = await utils.UsersDAL.user_coin_flow(user_id, coin_change, description)
#   return user

    user = session.query(UserEntity).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    coin_flow = UserCoinFlow(
        user_id = user.id,
        coin_change = coin_change,
        description = description,
        timestamp = current_timestamp
        )

    deduction_now = user.coin + coin_flow.coin_change

    if user:
        user.coin = deduction_now

    session.add(coin_flow)
    session.commit()

    return {
        "Deduction old":user.coin,
        "Deduction now":deduction_now
        }


