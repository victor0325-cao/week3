import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, Integer, BigInteger, String, DateTime

from .base import Base

class AdvisorForm(Base):

    __tablename__   = "advisor_logon"

    id              = Columb(BigInteger, primary_key=True)
    phone_number    = Column(String)
    password        = Column(String)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now())
