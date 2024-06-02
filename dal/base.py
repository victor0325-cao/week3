import json
import logging
import datetime

from enum import Enum
from typing import Dict, List, Union
from sqlalchemy import inspect, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAL:
    model = None

    @classmethod
    def get_start_end_time_by_date(cls, date):

        if not isinstance(date, datetime.date):
            date = datetime.strptime(date, "%Y-%m-%d")

        start_time = int(datetime.datetime.combine(date, datetime.datetime.min.time()).timestamp() * 1000)
        end_time = int(datetime.datetime.combine(date, datetime.datetime.max.time()).timestamp() * 1000)

        return start_time, end_time

    @classmethod
    def get_lastday(cls):
        now = datetime.datetime.now()

        today = datetime.datetime(now.year, now.month, now.day)
        lastday = today - datetime.timedelta(days=1)

        return lastday, today

    @classmethod
    async def batch_get_data_by_list(cls, func, id_list, batch=100):
        data = []

        for i in range(0, len(id_list), batch):
            data.extend(await func(id_list[i:i + batch]))

        return data

    @classmethod
    async def batch_get_data_by_date(cls, func, start_date, end_date, timedelta=datetime.timedelta(days=1)):
        data = []

        while start_date < end_date:
            _end_date = start_date + timedelta
            data.extend(await func(start_date, _end_date))
            start_date = _end_date

        return data

    @classmethod
    async def batch_get_data_by_timestamp(cls, func, start_time, end_time, timedelta=3600 * 24 * 1000):
        data = []

        while start_time < end_time:
            _end_time = min(start_time + timedelta, end_time)

            data.extend(await func(start_time, _end_time))

            start_time = _end_time

        return data

    @classmethod
    def to_dict(cls, raw_data, field_list=None):
        result = {}

        if raw_data is None:
            return result

        for attr in cls.columns(cls.model) if not field_list else field_list:
            result[attr] = getattr(raw_data, attr)

        return result

    @staticmethod
    def columns(model):
        return inspect(model).all_orm_descriptors.keys()

    @classmethod
    def add_model(cls, model, data):
        columns = cls.columns(cls.model)
        for k, v in data.items():
            if k in columns:

                if isinstance(v, Enum):
                    v = v.value

                try:
                    setattr(model, k, v)

                except Exception as err:
                    logging.exception(err)
                    raise

    @classmethod
    @property
    def all_attr_select(cls):
        return cls._gen_attr()

    @classmethod
    def _gen_attr(cls, fields=None):
        query = select(cls.model)

        if fields is not None:
            field_list = fields.split(',')
            if "id" not in field_list:
                field_list.append("id")

        else:
            field_list = cls.columns(cls.model)

        query = select(*[getattr(cls.model, field) for field in field_list])

        return query

    @classmethod
    def _gen_query(cls, query, where, sort="asc", sort_field="id", limit=None):
        for k, v in where.items():
            if v is None:
                continue

            if v == "sqlnull":
                query = query.where(getattr(cls.model, k).is_(None))
                continue

            if isinstance(v, Enum):
                v = v.value

            if k.endswith("@like") and isinstance(v, str):
                query = query.where(getattr(cls.model, k[:-5].strip()).like(f"%{v}%"))
                continue

            if k.endswith("@contains") and isinstance(v, str):
                query = query.where(func.json_contains(getattr(cls.model, k[:-9].strip()), json.dumps(v)))
                continue

            if k.endswith("!="):
                query = query.where(getattr(cls.model, k[:-2].strip()) != v)
                continue

            if k.endswith('>'):
                query = query.where(getattr(cls.model, k[:-1].strip()) > v)
                continue

            if k.endswith('>='):
                query = query.where(getattr(cls.model, k[:-2].strip()) >= v)
                continue

            if k.endswith('<'):
                query = query.where(getattr(cls.model, k[:-1].strip()) < v)
                continue

            if k.endswith('<='):
                query = query.where(getattr(cls.model, k[:-2].strip()) <= v)
                continue

            if isinstance(v, list):
                v = [_v.value if isinstance(_v, Enum) else _v for _v in v]
                query = query.where(getattr(cls.model, k).in_(v))
                continue

            query = query.where(getattr(cls.model, k) == v)

        if 'is_del' not in where and hasattr(cls.model, 'is_del'):
            query = query.where(cls.model.is_del == 0)

        s_field = getattr(cls.model, sort_field)

        if sort != 'asc':
            query = query.order_by(desc(s_field))

        if isinstance(limit, int):
            query = query.limit(limit)

        return query

    @classmethod
    async def find_one(cls, session: AsyncSession, fields: Union[str, None] = None, where: Dict = {},
                       sort: str = 'desc', sort_field: str = 'id'):
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

    @classmethod
    async def find_all(cls, session: AsyncSession, fields: Union[str, None] = None, where: Dict = {}, sort: str = 'asc',
                       sort_field: str = 'id', page: int = 1, count_per_page: int = 0, yield_batch=100, limit=None):
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

        return model_id

    @classmethod
    async def delete(cls, session: AsyncSession, model_id: int):
        return await cls.update(session, model_id, {'is_del': 1})

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


