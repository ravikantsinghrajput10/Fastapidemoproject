from users.models import UserModel
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from core.security import get_password_hash
from datetime import datetime


async def create_user_account(data, db):
    try:
        user = db.query(UserModel).filter(UserModel.email == data.email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    'status': '422',
                    'result': 'failure', 
                    'message': 'user already exists'
                }
            )

        new_user = UserModel(
            name=data.name,
            mobile_no=data.mobile_no,
            email=data.email,
            password=get_password_hash(data.password),
            is_active=0,
            is_verified=0,
            registered_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return JSONResponse(
            {
                'status':"201",
                'result':"success", 
                "message": "User created successfully", 
            },
            status_code=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            {
                'status':"400",
                'result':"failure", 
                "message": f"user creation failed: {str(e)}", 
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
