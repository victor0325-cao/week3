import josn
import copy

from sqlalchemy import func
from sqlalchemy import Column, Integer, DateTime, String, BigInteger

from .base import Base

class UserCoinFlow(Base):

    __tablename__   = "user_coin_flow"

    id              = Column(BigInteger, primary_key=True)
    coin_change     = Column(Integer)
    description     = Column(String)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now())
