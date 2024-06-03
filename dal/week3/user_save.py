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

class UserSaveDAL(BaseDAL):

    model = UserSave

    @classmethod
    @add_time_analysis
    @atomicity()
    async def save_advisor(cls, save, session=None):
        return await super().add(session, save)
