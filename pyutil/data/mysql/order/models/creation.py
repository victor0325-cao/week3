import json
import copy
  
from sqlalchemy import func, ForeignKey
from sqlalchemy import Column, BigInteger, Integer, String, Text, SmallInteger, DateTime
from sqlalchemy.orm import relationship

from pyutil.data.mysql.order.models.base import Base
  
class Creation(Base):
 
    __tablename__       = "user_order_creation"
 
    id                  = Column(BigInteger, primary_key=True)
    user_id             = Column(Integer, ForeignKey('user_info.id'))
    user_data           = relationship("UserEntity")
    general_situation   = Column(Text)
    specific_question   = Column(Text)
    attach_picture      = Column(String)
    order_id            = Column(Integer)
    order_time          = Column(String)
    delivery_time       = Column(String)
    status              = Column(SmallInteger, default=0)

