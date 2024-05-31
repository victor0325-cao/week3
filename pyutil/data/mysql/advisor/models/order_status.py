import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, BigInteger, String, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class AdvisorOrderStatus(Base):

    __tablename__   = "advisor_order_status"
    
    id              = Column(BigInteger, primary_key=True)
    advisor_home_id = Column(Integer,ForeignKey('adviser_home.id'))
    adviser_home_data = relationship("AdviserHome")
    name            = Column(String)
    order_status    = Column(Enum('work','idle'))

