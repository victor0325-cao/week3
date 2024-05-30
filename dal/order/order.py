import time
import json
import asyncio
import logging
import datetime

from sqlalchemy import distinct, select, func, desc, tuple_, join, and_

from pyutil.data.mysql.advisor.models import AdvisorInfo
from pyutil.data.mysql.user.models import UserInfo
from ..base import BaseDAL
from config import config

from pyutil.data.mysql.order.session import atomicity
from pyutil.data.mysql.order.models import *
from pyutil.decorators import add_time_analysis


class OrderCreateDAL(BaseDAL):

    model = Creation

    @classmethod
    @add_time_analysis
    @atomicity()
    async def add(cls, data, session=None):
        return await super().add(session, data)


class OrderListDAL(BaseDAL):

    model = None
    @classmethod
    @add_time_analysis
    @atomicity()
    async def order_list(cls, session=None):

        order = await session.execute(
            select(Creation).order_by(desc(Creation.id))
        )

        return order.scalars().all()
class OrderDetailsDAL(BaseDAL):

    model = None
    @classmethod
    @add_time_analysis
    @atomicity()
    async def order_details(cls, session=None):

        order = await session.execute(
            select(Creation).order_by(desc(Creation.id))
        )

        return order.scalars().all()

