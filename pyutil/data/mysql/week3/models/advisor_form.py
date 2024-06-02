import json
import copy

from sqlalchemy import Column, BigInteger, String

from .base import Base

class AdvisorForm(Base):

    __tablename__   = "adviser_logon"

    id              = Column(BigInteger, primary_key=True)
    phone_number    = Column(String)
    password        = Column(String)
