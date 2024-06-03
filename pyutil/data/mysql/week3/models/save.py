import json
import copy
  
from sqlalchemy import func, ForeignKey
from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.orm import relationship

from pyutil.data.mysql.week3.models.base import Base
  
class UserSave(Base):

    __tablename__   = "user_collection_adviser"

    id              = Column(BigInteger, primary_key =True)
    user_id         = Column(Integer, ForeignKey('user_info.id'))
    user_data       = relationship("UserInfo")
    adviser_id      = Column(Integer, ForeignKey('adviser_info.id'))
    adviser_data    = relationship("AdvisorInfo")
