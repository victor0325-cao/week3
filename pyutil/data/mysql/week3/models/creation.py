from sqlalchemy import ForeignKey
from sqlalchemy import Column, BigInteger, Integer, String, Text, Enum
from sqlalchemy.orm import relationship

from pyutil.data.mysql.week3.models.base import Base


class Creation(Base):
 
    __tablename__       = "user_order_creation"
 
    id                  = Column(BigInteger, primary_key=True)
    user_id             = Column(Integer, ForeignKey('user_info.id'))
    user_data           = relationship("UserInfo")
    general_situation   = Column(Text)
    specific_question   = Column(Text)
    attach_picture      = Column(String)
    order_id            = Column(Integer)
    order_time          = Column(String)
    delivery_time       = Column(String)
    status              = Column(Enum( 'Pending', 'Expired', 'Completed', 'Expedited', 'Timeout'))

