import json
import logging
import datetime

from enum import Enum
from typing import Dict, List, Union
from sqlalchemy import inspect, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

class BaseDAL:

    model=None

    @classmethod
    async def update(cls, session: AsyncSession, model_id: int, change_info: Dict = {}):
        model = (
            await session.execute(
                select(cls.model).where(cls.model.id == model_id)
            )
        ).scalar()

        if not model or (hasattr(cls.model, 'is_del') and cls.model.is_del == 1):
            return -1

        cls.add_model(model, change_info)

        await session.commit()

        model = model.__dict__

        return model





