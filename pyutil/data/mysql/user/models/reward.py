import json
import copy
from sqlalchemy import func, ForeignKey
from sqlalchemy import Column, Integer, BigInteger, DateTime, String, Float, Text
from sqlalchemy.orm import relationship

from pyutil.data.mysql.order.models.base import Base

class Reward(Base):

    __tablename__       = "user_order_reward"

    id                  = Column(BigInteger, primary_key=True)
    adviser_id          = Column(Integer, ForeignKey("adviser_reply.id"))
    adviser_data        = relationship("AdviserReply")
    rating              = Column(Float)
    write_review        = Column(Text)
    reward              = Column(Integer)
