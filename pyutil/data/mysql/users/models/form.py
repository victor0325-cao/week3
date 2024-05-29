import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, BigInteger, DateTime, String 

from .base import Base

class UserForm(Base):
    
    __tablename__   = "user_logon"

    id              = Column(BigInteger, primary_key=True)
    phone_number    = Column(String(100))
    password        = Column(String(100))
    created_at      = Column(DateTime, default= func.now())
    updated_at      = Column(DateTime, default= func.now())
