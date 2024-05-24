import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, BigInteger, Integer, Text, DateTime

from .base import Base

class AdvisorServiceSettings(Base):

    __tablename__       = "advisor_service_settings"

    id                  = Column(BigInteger, primary_key=True)
    amount_adjustment   = Column(String)
    service_adjustment  = Column(SmallInteger)
    created_at          = Column(DateTime, default=func.now())
    updated_at          = Column(DateTime, default=func.now())
