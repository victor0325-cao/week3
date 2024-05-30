import json
import copy
  
from sqlalchemy import func, ForeignKey
from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.orm import relationship

from pyutil.data.mysql.order.models.base import Base
  
class Save(Base):

    __tablename__   = "user_save_adviser"

    id              = Column(BigInteger, primary_key =True)
    user_id         = Column(Integer, ForeignKey('user_info.id'))
    user_data       = relationship("UserEntity")
    adviser_id      = Column(Integer, ForeignKey('adviser_info.id'))
    adviser_data    = relationship("AdviserEntity")
