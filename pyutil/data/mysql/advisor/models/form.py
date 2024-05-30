import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, Integer, BigInteger, String, DateTime

from .base import Base

class AdvisorForm(Base):

    __tablename__   = "advisor_logon"

    id              = Column(BigInteger, primary_key=True)
    phone_number    = Column(String)
    password        = Column(String)
