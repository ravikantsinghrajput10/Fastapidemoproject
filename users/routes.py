from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db
from users.schemas import CreateUserRequest
from users.services import create_user_account
from core.security import oauth2_scheme
from users.responses import UserResponse;

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

## User Registration
@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    result = await create_user_account(data=data, db=db)
    
    return result


@user_router.post('/list', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request):
    return request.user
