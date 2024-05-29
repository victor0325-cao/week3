import logging
from functools import wraps
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.sql import Update, Delete

from config import config

def create_async_mysql_engine(conf, is_slave=False):
    engine = create_async_engine(
        'mysql+aiomysql://{}:{}@{}:3025/{}?charset=utf8mb4'.format(
             conf.username,
             conf.password,
             conf.host,
             conf.db_name, 
             ),
        pool_size = int(conf.pool_size),
        pool_recycle = 3600,
        pool_pre_ping = True
    )

    return engine
Session = sessionmaker(class_=AsyncSession)

@asynccontextmanager
async def open_session(async_session_cls=Session, commit=False):
    async_session = async_session_cls()
    try:
        yield async_session

        if commit:
            await async_session.commit()

    except:
        await async_session.rollback()
        raise

    finally:
        await async_session.close()

def atomicity(commit=False):
    def wrapper(func):
        @wraps(func)
        async def decorator(*args, **kwargs):
            session = kwargs.get('session')
            if not session:
                async with open_session(Session, commit=commit) as session:
                    kwargs['session'] = session
                    r = await func(*args, **kwargs)
            else:
                r = await func(*args, **kwargs)
            return r
        return decorator
    return wrapper

