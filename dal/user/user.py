import time
import json
import asyncio
import logging
import datetime
import copy
from sqlalchemy import distinct, select, func, desc
from sqlalchemy.orm.attributes import flag_modified

from ..base import BaseDAL
from config import config
from pyutil.data.mysql.user.models import *
from pyutil.data.mysql.user.session import atomicity

from schemas.exceptions import *
from pyutil.decorators import add_time_analysis

class UserFormDAL(BaseDAL):

    model = UserForm
    
    @classmethod
    @add_time_analysis
    @atomicity()
    async def add(cls, data, session=None):
        return await super().add(session, data)

class UserDAL(BaseDAL):

    model = UserInfo
    
    @classmethod
    @add_time_analysis
    @atomicity()
    async def update_user(cls, user_id, session=None):
        
        user_entity = await cls.update(
            session,
            fieldes="user_id",
            where={
                "user_id": user_id
            }
        )

        return user_entity

    @clsssmethod
    @add_time_analysis
    @atomicity()
    async def user(cls, user_id, session=None):

        user = await cls.find_one(
            session,
            fiedes="user_id",
        )

class UserListDAL(BaseDAL):

    model = None

    @classmethod
    @add_time_analysis
    @atomicity()
    async def user_advisor_list(cls, session=None):

        advisor_list = await cls.find_all(
            session,
            fieldes = "advisor_id",
            where={
                "advisor_id": advisor_id,
            }
        )

        return advisor_list

class UserAdvisorHomeDAL(BaseDAL):

    model = None

    @classmethod
    @add_time_analysis
    @atomicity()
    async def user_advisor_home(cls, session=None):

        advisor_home = await cls.find_one(
            session,
            fieldes = "advisor_id",
            where={
                "advisor_id": advisor_id,
            }
        )

        return advisor_home

class SaveDAL(BaseDAL):

    model = Save

    @classmethod
    @add_time_analysis
    @atomicity()
    async def save_advisor(cls, user_id, session=None):

        collection = await cls.update(
            session,
            fieldes = "user_id,adviser_id",
            where={
                "user_id": user_id,
            }
        )

        return collection

class CoinFlowDAL(BaseDAL):

    model = UserCoinFlow

    @classmethod
    @add_time_analysis
    @atomicity()
    async def user_coin_flow(cls, user_id, coin_change, description,session=None):

        user = await cls.update(
            session,
            fieldes = "user_id,coin_change,description",
            where={
                "user_id": user_id,
                "coin_change": coin_change,
                "description": description,
            }
        )

        return user
