import json
import copy

from sqlalchemy import func, ForeignKey
from sqlalchemy import Column, Integer, DateTime, String, BigInteger
from sqlalchemy.dialects.mysql import TIMESTAMP

from .base import Base

class UserCoinFlow(Base):

    __tablename__   = "user_coin_flow"

    id              = Column(BigInteger, primary_key=True)
    user_id         = Column(Integer, ForeignKey('user_info.id'))
    coin_change     = Column(Integer)
    description     = Column(String)
    timestamp       = Column(TIMESTAMP)
