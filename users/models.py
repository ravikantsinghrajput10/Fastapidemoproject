from sqlalchemy import Column, Integer,Float, String, DateTime, func
from datetime import datetime
from core.database import Base



class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300))
    mobile_no = Column(Integer)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(300))
    is_active = Column(Integer, default=1)  
    is_verified = Column(Integer, default=1)
    verified_at = Column(DateTime, nullable=True, default=None)
    registered_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    amount = Column(Float)

    