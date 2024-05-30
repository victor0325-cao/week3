import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, BigInteger, Integer, Text, DateTime, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class AdvisorServiceSettings(Base):

    __tablename__       = "advisor_service_settings"

    id                  = Column(BigInteger, primary_key=True)
    advisor_id          = Column(Integer, ForeignKey('advisor_info.id'))
    advisor_data        = relationship("AdvisorInfo")
    amount_adjustment   = Column(String)
    service_adjustment  = Column(SmallInteger)
