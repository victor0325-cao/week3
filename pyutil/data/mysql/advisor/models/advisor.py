import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime

from .base import Base

class AdvisorInfo(Base):

    __tablename__   = "advisor_info"

    id              = Column(BigInteger, primary_key = True)
    name            = Column(String)
    bio             = Column(Text)
    work            = Column(String)
    about           = Column(Text)
