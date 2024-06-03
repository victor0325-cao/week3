import time
import json
import asyncio
import logging
import datetime
import copy
from typing import Dict

from sqlalchemy import distinct, select, func, desc
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime

from pyutil.data.mysql.week3.models import AdvisorInfo
from ..base import BaseDAL
from config import config
from pyutil.data.mysql.week3.models import *
from pyutil.data.mysql.week3.session import atomicity

from schemas.exceptions import *
from pyutil.decorators import add_time_analysis

class UserAdvisorFormDAL(BaseDAL):
    model = AdvisorInfo

    @classmethod
    @add_time_analysis
    @atomicity()
    async def user_advisor_list(cls, session=None):
        advisor_list = await cls.find_all(
            session,
            fields='name,bio'
        )
        return advisor_list


    @classmethod
    @add_time_analysis
    @atomicity()
    async def user_advisor_home(cls, advisor_id, session=None):
        advisor_home = await cls.find_one(
            session,
            fields="name,bio,work,about",
            where={
                "id": advisor_id,
            }
        )
        return advisor_home
