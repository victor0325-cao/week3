import josn
import copy

from sqlslchemy import func
from sqlalchemy import Column, BigInteger, DateTime, String 

from .base import Base

class UserForm(Base):
    
    __tablename__   = "user_logon"

    id              = Column(BigInteger, primary_key=True)
    phone_number    = Column(String(100))
    password        = Column(String(100))
    created_at      = Column(DateTime, default=Func.now())
    updated_at      = Column(DateTime, default= Func.now())
