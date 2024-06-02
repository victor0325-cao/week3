import time
import json
import asyncio
import logging
import datetime
import copy
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


class UserDAL(BaseDAL):
    model = UserInfo

    @classmethod
    @add_time_analysis
    @atomicity()
    async def update_user(cls, user_id, user, session=None):
        return await super().update(session, user_id, user)

    @classmethod
    @add_time_analysis
    @atomicity()
    async def user(cls, id, session=None):
        user = await cls.find_one(
            session,
            where={
                "id": id
            }
        )
        return user


class UserListDAL(BaseDAL):
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


class UserAdvisorHomeDAL(BaseDAL):
    model = AdvisorInfo

    @classmethod
    @add_time_analysis
    @atomicity()
    async def user_advisor_home(cls, adviser_id, session=None):

        advisor_home = await cls.find_one(
            session,
            fields="name,bio,work,about",
            where={
                "advisor_id": adviser_id,
            }
        )
        return advisor_home


class SaveDAL(BaseDAL):
    model = Save

    @classmethod
    @add_time_analysis
    @atomicity()
    async def save_advisor(cls, save, session=None):
        return await super().add(session, save)


class CoinFlowDAL(BaseDAL):
    model = UserCoinFlow

    @classmethod
    @add_time_analysis
    @atomicity()
    async def user_coin_flow(cls, coin_flow, session=None):
        return await super().add(session, coin_flow)
