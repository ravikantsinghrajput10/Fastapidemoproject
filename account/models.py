from sqlalchemy import Column, Integer,ForeignKey,Float, String, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    transaction_type = Column(String)
    transaction_mode = Column(String)
    balance = Column(Float)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    