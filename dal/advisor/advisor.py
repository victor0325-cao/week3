import time
import json
import asyncio
import logging
import datetime

from typing import Dict
from sqlalchemy import distinct, select, func, desc

from ..base import BaseDAL
from config import config

from pyutil.data.mysql.advisor.session import atomicity
from pyutil.data.mysql.advisor.models import AdvisorInfo
from pyutil.decorators import add_time_analysis

class AdvisorDAL(BaseDAL):

    model = AdvisorInfo

    @classmethod
    @add_time_analysis
    @atomicity()
    async def add(cls, data, session=None):
        return await super().add(session, data)

    @classmethod
    @add_time_analysis
    @atomicity()
    async def update_advisor(cls, advisor_id, session=None):
        
        advisors =await cls.update(
            session,
            model_id = advisor_id,
            change_info = {
                "name":name,
                "bio":bio,
                "work":work,
                "about":about,
                }
        )

        return advisor
    
    @classmethod
    @add_time_analysis
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
    @add_time_analysis
    @atomicity()
    async def update_advisor(cls, advisor_id, session=None):
        
        advisor_entity = cls.update(
            session,
            model_id = advisor_id,
            change_info={
                "advisor_id": advisor_id,
            }
        )

        return advisor_entity

    @classmethod
    @add_time_analysis
    @atomicity()
    async def update_service(cls, advisor_id, session=None):
        
        service = await cls.update(
            session,
            model_id = advisor_id,
            change_info={
                "advisor_id":advisor_id,
            },
            limit = 1,
        )

        return service
    
    @classmethod
    @add_time_analysis
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





