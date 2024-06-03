import time
import json
import asyncio
import logging
import datetime

from typing import Dict
from sqlalchemy import distinct, select, func, desc, asc

from ..base import BaseDAL
from config import config

from pyutil.data.mysql.week3.session import atomicity
from pyutil.data.mysql.week3.models import *
from pyutil.decorators import add_time_analysis


class AdvisorlogonDAL(BaseDAL):
    
    model = AdvisorForm

    @classmethod
    @add_time_analysis
    @atomicity()
    async def add(cls, data, session=None):
        return await super().add(session, data)


class InfoUpdateDAL(BaseDAL):
    
    model = AdvisorInfo

    @classmethod
    @add_time_analysis
    @atomicity()
    async def update_advisor(cls, advisor_id, advisor, session=None):
        return await super().update(session, advisor_id, advisor)


class AdvisorHomeDAL(BaseDAL):
    
    model = AdvisorHome

    @classmethod
    @add_time_analysis
    @atomicity()
    async def advisor_home(cls, session=None):
        advisor =await cls.find_all(
            session,
            fields="name",
        )
        return advisor


class TakeOrderUpdateDAL(BaseDAL):
    
    model = AdvisorOrderStatus


    @classmethod
    @add_time_analysis
    @atomicity()
    async def update_advisor(cls, advisor_id, advisor, session=None):
        return await super().update(session, advisor_id, advisor)


class ServiceUpdateDAL(BaseDAL):
    
    model = AdvisorServiceSettings

    @classmethod
    @add_time_analysis
    @atomicity()
    async def update_service(cls, advisor_id, adviser, session=None):
        return await super().update(session, advisor_id, adviser)


class AdvisorReplyDAL(BaseDAL):
    
    model = AdvisorReply

    @classmethod
    @add_time_analysis
    @atomicity()
    async def reply_user(cls, new_reply, session=None):
       return await super().add(session, new_reply)
