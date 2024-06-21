from pydantic import BaseModel,validator

class TransactionSchema(BaseModel):
    amount: float
    transaction_mode: str
    user_id: int


    @validator('amount')
    def amount_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Amount must be greater than zero')
        return value


    @validator('transaction_mode')
    def transaction_mode_must_be_valid(cls, value):
        if value not in ['UPI', 'CASH', 'CARD']:
            raise ValueError('Transaction mode must be either UPI, CASH, or CARD')
        return value
    

    @validator('user_id')
    def user_id_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('User ID must be greater than zero')
        return value
    
    # class Config:
    #     orm_mode = True
    
