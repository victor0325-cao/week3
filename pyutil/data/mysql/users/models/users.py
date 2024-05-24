import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, BigInteger, DateTime, String, Integer, Text

from .base import Base 

class UserInfo(Base):
    
    __tablename__ = "user_info"
    
    id            = Column(BigInteger, primary_key=True)
    name          = Column(String)
    birth         = Column(String)
    gender        = Column(String)
    bio           = Column(Text)
    about         = Column(Text)
    coin          = Column(Integer)
    created_at    = Column(DateTime, default=Func.now())
    updated_at    = Column(DateTime, default=Func.now())
