import json
import copy

from sqlalchemy import Column, BigInteger, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class AdvisorServiceSettings(Base):

    __tablename__       = "adviser_service_settings"

    id                  = Column(BigInteger, primary_key=True)
    advisor_id          = Column(Integer, ForeignKey('adviser_info.id'))
    advisor_data        = relationship("AdvisorInfo")
    amount_adjustment   = Column(String)
    service_adjustment  = Column(Enum( 'open','close'))
