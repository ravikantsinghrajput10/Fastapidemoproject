import re
from pydantic import BaseModel, EmailStr,validator

class CreateUserRequest(BaseModel):
    name: str
    mobile_no: int
    email: EmailStr
    password: str

    @validator('name')
    def name_must_not_be_empty(cls, value):
        if not value.strip():  
            raise ValueError('Name must not be empty')
        if not value.isalpha():  
            raise ValueError('Name must only contain alphabetic characters')
        return value


    @validator('mobile_no')
    def mobile_no_must_be_valid(cls, value):
        if len(str(value)) != 10: 
            raise ValueError('Mobile number must be 10 digits long')
        return value

    @validator('email')
    def email_must_be_valid(cls, value):
        
        return value

    @validator('password')
    def password_requirements(cls, value):
        
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')
        
        if not re.search(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', value):
            raise ValueError('Password must contain at least one alphabetic character, one numeric character, and one special character')
        
        return value