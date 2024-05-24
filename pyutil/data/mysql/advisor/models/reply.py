import json
import copy

from sqlalchemy import func
from sqlalchemy import Column, BigInteger, Integer, Text, DateTime

from .base import Base

class AdvisorReply(Base):

    __tablename__   = "advisor_reply"

    id              = Column(BigInteger, primary_key=True)
    reply_text      = Column(Text)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now())
