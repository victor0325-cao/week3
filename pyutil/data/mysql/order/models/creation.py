import json
import copy
  
from sqlalchemy import func
from sqlalchemy import Column, BigInteger, Integer, String, Text, SmallInteger
  
from .base import Base
  
class UserOrderCreation(Base):
 
    __tablename__       = "user_order_creation"
 
    id                  = Column(BigInteger, primary_key=True)
    general_situation   = Column(Text)
    specific_question   = Column(Text)
    status              = Column(SmallInteger, default=0)
    created_at          = Column(DateTime, default=func.now())
    updated_at          = Column(DateTime, default=func.now())
