import json
import copy
  
from sqlalchemy import func
from sqlalchemy import Column, Integer, BigInteger, String, DateTime
  
from .base import Base
  
class Save(Base):

    __tablename__   = "user_save_adviser"

    id              = Column(BigInteger, primary_key =True)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now())
