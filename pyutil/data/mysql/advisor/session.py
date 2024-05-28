import logging
from functools import wraps
from contextlib import asynccontestmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemt.sql import Update, Delete

from config import config

##设置连接池
def create_async_mysql_engine(conf, is_slave=False):
    engine = create_async_engine(
        'mysql+aiomysql://{}:{}@{}:3306/{}?charset=utf8mb4'.format(
             conf.username,
             conf.password,
             conf.host,
             conf.db_name, 
             ),
        pool_size = int(conf.pool_size),  #设置连接池大小
        pool_recycle = 3600,              #定义连接池中的连接回收时间
        pool_pre_ping = True              #启用或禁用连接池中的连接在使用前的自检测功能，True表示启用
    )

    return engine

Session = sessionmaker(class_=AsyncSession, sync_session_class=RoutingSession)

#@asynccontextmanager
# 装饰器：定义了一个异步上下文管理器 open_session，用于异步打开会话。
# 在这个上下文管理器中，会为提供的异步会话类创建一个会话实例，提供一个会话对象供调用方执行数据库操作。
# 如果设置了 commit=True，则在 with 块结束时会自动提交事务；否则，会回滚事务。
# 最后，无论如何，都会关闭会话。
 
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

#atomicity
# 装饰器函数：定义了一个装饰器，用于确保函数执行的原子性。
# 如果传入的函数没有指定会话（session），则会在执行函数前创建一个会话，将该会话作为参数传递给函数。
# 在装饰的函数执行完毕后，会根据情况进行提交或回滚，并关闭会话。
# 最终返回函数执行结果。
 
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
