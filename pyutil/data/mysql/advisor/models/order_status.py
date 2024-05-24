import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, BigInteger, String, Integer, SmallInteger, DateTime

from .base import Base

class AdvisorOrderStatus(Base):

    __tablename__   = "advisor_order_status"
    
    id              = Column(BigInteger, primary_key=True)
    name            = Column(String)
    status          = Column(SmallInteger)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now())
