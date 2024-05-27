import time
import json
import asyncio
import logging
import datetime

from sqlalchemy import distinct, select, func, desc
from fastapi_cache.decorator import cache

from ..base import BaseDAL
from config import config

from pyutil.data.mysql.healux_admin.session import atomicity
from pyutil.data.mysql.healux_admin.models import Advisors
from pyutil.decorators import add_time_analysis

class AdvisorsDAL(BaseDAL):

    model = Advisors

    @classmethod
    @add_time_analysis
    @atomicity()
    async def update_adviser(cls, session=None):
        advisors = session.query(Adviser)
