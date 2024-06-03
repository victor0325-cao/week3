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


class UserFormDAL(BaseDAL):

    model = UserForm

    @classmethod
    @add_time_analysis
    @atomicity()
    async def add(cls, data, session=None):
        return await super().add(session, data)


    @classmethod
    @add_time_analysis
    @atomicity()
    async def post_token(cls,message,session=None):
        user = await cls.find_one(
            session,
            where={
                "phone_number": message.phone_number,
                "password":message.password
            }
        )
        if not user or user.password != login_form.password:
            raise HTTPException(status_code = 401,
                detail = "Incorrect phone_number or password",
                headers = {"WWW-Authenticate": "Bearer"})
            
            return user
        
