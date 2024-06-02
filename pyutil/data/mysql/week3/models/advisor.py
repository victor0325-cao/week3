import json
import copy

from sqlalchemy import Column, BigInteger,String, Text

from .base import Base

class AdvisorInfo(Base):

    __tablename__   = "adviser_info"

    id              = Column(BigInteger, primary_key = True)
    name            = Column(String)
    bio             = Column(Text)
    work            = Column(String)
    about           = Column(Text)
