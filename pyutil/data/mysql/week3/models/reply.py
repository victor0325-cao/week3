import json
import copy

from sqlalchemy import Column, BigInteger, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class AdvisorReply(Base):

    __tablename__   = "adviser_reply"

    id              = Column(BigInteger, primary_key=True)
    adviser_id      = Column(Integer, ForeignKey('adviser_home.id'))
    adviser         = relationship("AdvisorHome")
    order_id        = Column(Integer, ForeignKey('user_order_creation.id'))
    user_order      = relationship("Creation")
    reply_text      = Column(Text)
