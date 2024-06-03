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

class AdvisorHomeDAL(BaseDAL):
    
    model = AdvisorHome

    @classmethod
    @add_time_analysis
    @atomicity()
    async def get_advisor_home(cls, session=None):
        advisor =await cls.find_all(
            session,
            fields="name",
        )
        return advisor
