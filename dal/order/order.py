import time
import json
import asyncio
import logging
import datetime

from sqlalchemy import distinct, select, func, desc, tuple_, join, and_

from pyutil.data.mysql.week3.models import AdvisorInfo
from pyutil.data.mysql.week3.models import UserInfo
from ..base import BaseDAL
from config import config

from pyutil.data.mysql.week3.session import atomicity
from pyutil.data.mysql.week3.models import *
from pyutil.decorators import add_time_analysis


class OrderDAL(BaseDAL):

    model = Creation

    @classmethod
    @add_time_analysis
    @atomicity()
    async def add(cls, data, session=None):
        return await super().add(session, data)

    @classmethod
    @add_time_analysis
    @atomicity()
    async def order_list(cls,n=10, session=None):

        order = await cls.find_all(
            session,
            fields= "order_time,specific_question,status",
            where= {
                "status": "Pending"
            },
            limit=n,
        )
        return order

    @classmethod
    @add_time_analysis
    @atomicity()
    async def order_details(cls, user_id, session=None):

        order = await cls.find_one(
            session,
            where= {
                "user_id": user_id
            }
        )

        return order