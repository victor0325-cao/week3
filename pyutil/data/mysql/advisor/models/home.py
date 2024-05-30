import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, Integer, BigInteger, DateTime, String, Float, Text

from .base import Base

class AdvisorHome(Base):

    __tablename__   = "advisor_home"

    id              = Column(BigInteger, primary_key=True)
    name            = Column(String)
    coin            = Column(Integer)
    work_state      = Column(String)
    readings        = Column(Integer)
    score           = Column(Integer)
    comments        = Column(Integer)
    on_time         = Column(Float)
    reviews         = Column(Text)
    complete        = Column(Integer)
