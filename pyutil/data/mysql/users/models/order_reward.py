import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, Integer, BigInteger, DateTime, String, Float

from .base import Base

class UserOrderReward(Base):

    __tablename__       = "user_order_reward"

    id                  = Column(BigInteger, primary_key=True)
    rating              = Column(Float)
    write_review        = Column(Text)
    reward              = Column(Integer)
    created_at          = Column(DateTime, default=func.now())
    updated_at          = Columb(DateTime, default=func.now())
