import time
import json
import asyncio
import logging
import datetime

from sqlalchemy import distinct, select, func, desc
from fastapi_cache.decorator import cache

from ..base import BaseDAL
from config import config

from pyutil.data.mysql.Advisor.session import atomicity
from pyutil.data.mysql.Advisor.models import Advisors
from pyutil.decorators import add_time_analysis

class AdvisorsDAL(BaseDAL):

    model = Advisors

    @classmethod
    @add_time_analysis
    @atomicity()
    async def update_advisor(cls, advisor_id, session=None):
        
        advisors =await cls.update(
            session,
            fields="name,bio,work,about",
            where={
                "advisor_id":advisor_id
            }

        return advisor
    
    @classmethod
    @add_time_anlysis
    @atomicity()
    async def advisor_home(cls, advisor_id, session=None):

        advisor = await cls.find_one(
            session,
            fields="advisor_id",
            where={
               "advisor_id": advisor_id,
            } 
        )

        return advisor

    @classmethod
    @add_time_anlysis
    @atomicity()
    async def update_advisor(cls, advisor_id, session=None):
        
        advisor_entity = cls.update(
            session,
            fields="advisor_id",
            where={
                "advisor_id": advisor_id,
            }
        )

        return advisor_entity

    @classmethod
    @add_time_anlysis
    @atomicity()
    async def update_service(cls, advisor_id, session=None):
        
        service = await cls.update(
            session,
            fields="advisor_id",
            where={
                "advisor_id":advisor_id,
            }
            limit = 1
        )

        return service
    
    @classmethod
    @add_time_anlysis
    @atomicity()
    async def reply_user(cls, advisor_id, order_id, session=None):
        
        user_order = await cls.add(
            session,
            fields="advisor_id,order_id",
            where={
                "advisor_id": advisor_id,
                "order_id": order_id,
            }
        )

        return user_order





