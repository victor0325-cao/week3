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

class InfoUpdateDAL(BaseDAL):
    
    model = AdvisorInfo

    @classmethod
    @add_time_analysis
    @atomicity()
    async def update_advisor(cls, advisor_id, advisor, session=None):
        return await super().update(session, advisor_id, advisor)
