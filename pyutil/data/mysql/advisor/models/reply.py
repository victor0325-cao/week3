import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, BigInteger, Integer, Text, DateTime, ForeignKey

from sqlalchemy.orm import relationship

from .base import Base

class AdvisorReply(Base):

    __tablename__   = "advisor_reply"

    id              = Column(BigInteger, primary_key=True)
    adviser_id      = Column(Integer, ForeignKey('adviser_home.id'))
    adviser         = relationship("AdviserHome")
    order_id        = Column(Integer, ForeignKey('user_order_creation.id'))
    user_order      = relationship("UserOrderCreation")
    reply_text      = Column(Text)
