import json
import logging
import datetime

from enum import Enum
from typing import Dict, List, Union
from sqlalchemy import inspect, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

class BaseDAL:

    model=None
#修改
    @classmethod
    async def update(cls, session:AsyncSession, model_id: int, change_info: Dict = {}):
        model = (
            await session.execute(
                select(cls.model).where(cls.model.id == model_id)
            )
        ).scalsr()

        cls.add_model(model, change_info)

        await session.commit()
        return model_id
#添加
    @classmethod
    async def add(cls, session: AsyncSession, data: List[Dict] = [{}]):
        if not data:
            return -1

        if not isinstance(data, list):
            data = [data]

        model_ids = []
        for d in data:
            model = cls.model()
            cls.add_model(model, d)
            session.add(model)
            await session.flush()

            model_ids.append(model.id)

        await session.commit()

        return model_ids[0] if len(model_ids) == 1 else model_ids
#查询一条
    @classmethod
    async def find_one(cls, session: AsyncSession, fields: Union[str, None] = None, where: Dict = {}, sort: str = 'desc', sort_field: str = 'id'):
        query = cls._gen_query(
            cls._gen_attr(fields),
            where,
            sort,
            sort_field
        )

        result = (
            await session.execute(query)
        ).first()

        return result
#查询所有
    @classmethod
    async def find_all(cls, session: AsyncSession, fields: Union[str, None] = None, where:Dict = {}, sort: str = 'asc', sort_field: str = 'id', page: int = 1, count_per_page: int = 0, yield_batch=100, limit=None):
        offset = (page - 1) * count_per_page

        query = cls._gen_query(
            cls._gen_attr(fields),
            where,
            sort,
            sort_field,
            limit
        )

        result = []

        if count_per_page > 0:
            total = (
                await session.execute(
                    cls._gen_query(
                        select(func.count()),
                        where
                    )
                )
            ).scalar()

            page_items = await session.execute(query.offset(offset).limit(count_per_page))
            for item in page_items.yield_per(yield_batch):
                result.append(item)

            return {
                "data": result,
                "total": total,
                "page": page,
                "size": count_per_page
            }
        else:
            items = await session.execute(query)
            for item in items.yield_per(yield_batch):
                result.append(item)

            return result

