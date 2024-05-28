import time
import json
import asyncio
import logging
import datetime
import copy
from sqlalchemy import distinct, select, func, desc
from sqlalchemy.orm.attributes import flag_modified
from fastapi_cache.decorator import cache

from ..base import BaseDAL
from config import config
from pyutil.data.mysql.users.models import Star

from schemas.constant import *
from schemas.exceptions import *
from pyutil.data.mysql.users.session import atomicity
from pyutil.decorators import add_time_analysis

class UsersDAL(BaseDAL):

    model = Users

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


    @classmethod
    @add_time_analysis
    @atomicity()
    async def collection_advisor(cls, user_id, session=None):

        collection = await cls.update(
            session,
            fieldes = "user_id,adviser_id",
            where={
                "user_id": user_id,
            }
        )

        return collection


    @classmethod
    @add_time_analysis
    @atomicity()
    async def user_coin_flow(cls, user_id, coin_change, description):

        user = await cls.update(
            session,
            fieldes = "user_id,coin_change,description",
            where={
                "user_id": user_id,
                "coin_change": cpin_change,
                "description": description,
            }
        )

        return user
