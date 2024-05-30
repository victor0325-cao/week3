import json
import logging
import datetime

from enum import Enum
from pydoc import text
from typing import Dict, List, Union
from sqlalchemy import inspect, desc, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

class BaseDAL:

    model=None
    
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

            query  = query.where(getattr(cls.model, k) == v)

        if 'is_del' not in where and hasattr(cls.model, 'is_del'):
            query = query.where(cls.model.is_del == 0)

        s_field = getattr(cls.model, sort_field)

        if sort != 'asc':

            query = query.order_by(desc(s_field))

        if isinstance(limit, int):
            query = query.limit(limit)

        return query

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


    @classmethod
    async def find_one(cls, session: AsyncSession, fields: Union[str, None] = None, where: Dict = {}):
        query = cls._gen_query(
            cls._gen_attr(fields),
            where
        )

        result = (
            await session.execute(query, bind=session.get_bind(cls.model))
        ).first()
        return result


    @classmethod
    async def find_all(cls, session: AsyncSession, fields: Union[str, None] = None, where:Dict = {}, sort: str = 'asc',  limit=None):

        if not fields: 
            raise ValueError("Fields cannot be empty")

        clean_fields = cls.clean_and_validate_fields(fields)

        try:
            results = await session.query(*clean_fields)
            for result in results:
                yield result
        except SQLAlchemyError as e:

            print(f"Database error occurred: {e}")

            raise
        except Exception as e:

            print(f"An unexpected error occurred: {e}")
            raise

    @classmethod
    def clean_and_validate_fields(cls, fields: Union[str, None] = None):
        clean_fields = [field.strip() for field in fields if field.strip()]
        return clean_fields 





