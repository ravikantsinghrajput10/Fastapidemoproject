from fastapi import status, Depends, Request,HTTPException
from fastapi.responses import JSONResponse
from account.models import Transaction
from users.models import UserModel
from fastapi.exceptions import HTTPException
from core.security import get_password_hash
from datetime import datetime


async def add_money(data, db):
    try:
        getDtls = db.query(UserModel).filter(UserModel.id == data.user_id).first() 
        
        if not getDtls:
            return JSONResponse(
                {
                    'status':'404',
                    'result':"success", 
                    'message': 'Record not found'
                }, 
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        if getDtls.amount is None:
            balance = data.amount
        else : 
            balance = (getDtls.amount + data.amount)

        transaction_type = 'Credited'

        db_transaction = Transaction(
            user_id=data.user_id,
            amount=data.amount,
            transaction_mode=data.transaction_mode,
            transaction_type = transaction_type,
            balance = balance,
            updated_at=datetime.now()
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        # Update Amount In Main Acount Like In User Table Column
        getDtls.amount = balance
        db.commit()
        

        return JSONResponse(
            {
                'status':"201",
                'result':"success", 
                "message": "Transaction completed successfully", 
            },
            status_code=status.HTTP_201_CREATED
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            {
                    'status':"400",
                    'result':"failure", 
                    "message": f"Transaction failed: {str(e)}", 
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
        
async def remove_money(data, db):

    try:

        getDtls = db.query(UserModel).filter(UserModel.id == data.user_id).first() 

        if not getDtls:
            return JSONResponse(
                {
                    'status':'404',
                    'result':"success", 
                    'message': 'Record not found'
                }, 
                status_code=status.HTTP_404_NOT_FOUND
            )

        if getDtls.amount is None or getDtls.amount < data.amount:
            return JSONResponse(
                {
                    'status':'200',
                    'result':"success", 
                    'message': 'Insufficient fund in account'
                }, 
                status_code=status.HTTP_200_OK
            )
        else : 
            balance = (getDtls.amount - data.amount)

        transaction_type = 'Debited'

        db_transaction = Transaction(
            user_id=data.user_id,
            amount=data.amount,
            transaction_mode=data.transaction_mode,
            transaction_type = transaction_type,
            balance = balance,
            updated_at=datetime.now()
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)

        # Update Amount In Main Acount Like In User Table Column
        getDtls.amount = balance
        db.commit()

        return JSONResponse(
            {
                'status':"201",
                'result':"success", 
                "message": "Transaction completed successfully", 
            },
            status_code=status.HTTP_201_CREATED
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'status':"400",
                'result':"failure", 
                "message": f"Transaction failed: {str(e)}", 
            }
        )



