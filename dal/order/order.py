import time
import json
import asyncio
import logging
import datetime

from sqlalchemy import distinct, select, func, desc, tuple_, join, and_
#from fastapi_cache.decorator import cache

from ..base import BaseDAL
from config import config

from pyutil.data.mysql.order.session import atomicity
from pyutil.data.mysql.order.models import *
from pyutil.decorators import add_time_analysis


class OrderDAL(BaseDAL):

    model = Order

    @classmethod
    @atomicity()
    @add_time_analysis
    async def order_list(cls, session=None):

        order = await cls.find_all(
            session,
            fields="order_id",
            )
        return order

    @classmethod
    @atomicity()
    @add_time_analysis
    async def order_details(cls, session=None):
        
        order = await cls.find_one(
            session,
            fields="order_id",
            where={
                "order_id": order_id,
            }
            )
