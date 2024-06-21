from fastapi import APIRouter, status, Depends, Request,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db
from account.schemas import TransactionSchema
from account.services import add_money,remove_money
from core.security import oauth2_scheme
from account.responses import AccountResponse;
from typing import List
from account.models import Transaction
from users.models import UserModel

router = APIRouter(
    prefix="/account",
    tags=["Account"],
    responses={404: {"description": "Not found"}},
)


### ADD MONEY IN USER ACCOUNT
@router.post('/add', status_code=status.HTTP_201_CREATED)
async def addMoney(data: TransactionSchema, db: Session = Depends(get_db)):
    result = await add_money(data=data, db=db)
    
    return result


### REMOVE MONEY FROM USER ACCOUNT
@router.post('/remove', status_code=status.HTTP_201_CREATED)
async def removeMoney(data: TransactionSchema, db: Session = Depends(get_db)):
    result = await remove_money(data=data, db=db)
    
    return result



### GET USER BALANCE
@router.get('/balance', status_code=status.HTTP_200_OK, response_model=AccountResponse)
async def userBalance(request: Request, user_id:int, db: Session = Depends(get_db)):
    userBalance = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not userBalance :
        return JSONResponse(
            {
                'status':'404',
                'result':"success", 
                'message': 'Record not found'
            }, 
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    return JSONResponse(
        {
                'status':"200",
                'result':"success", 
                "message": "Account Balance", 
                "Amount": userBalance.amount
        },
        status_code=status.HTTP_200_OK
    )

    
 ### GET TRANSACTION HISTORY OF USER    
@router.get('/history/{user_id}', status_code=status.HTTP_200_OK, response_model=AccountResponse)
def get_transaction(request: Request, user_id:int, db: Session = Depends(get_db)):
    transactionHistory = db.query(Transaction).filter(Transaction.user_id == user_id).all()

    if not transactionHistory:
        return JSONResponse(
            {
                'status':'404',
                'result':"success", 
                'message': 'Record not found'
            }, 
            status_code=status.HTTP_404_NOT_FOUND
        )

    transactionList = []
    for item in transactionHistory :
        data= {
            "transaction_id": item.id,
            "amount": item.amount,
            "transaction_type": item.transaction_type,
            "transaction_mode": item.transaction_mode
        }

        transactionList.append(data)
    
    return JSONResponse(
        {
            'status':"200",
            'result':"success", 
            "message": "Transaction History", 
            "transactionHistory": transactionList
        },
        status_code=status.HTTP_200_OK
    )
