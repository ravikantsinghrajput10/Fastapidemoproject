from pydantic import BaseModel 
from typing import Union
from datetime import datetime

class BaseResponse(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class AccountResponse(BaseModel):
    id: int
    amount: float
    transaction_type: str
    user_id: int
   