from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from schemas import user_schema, token_schema
from services import users_service
from helpers import authentication
from routers.oauth2 import check_credentials


router = APIRouter(prefix='/users',tags=['Users'])


@router.get("/", response_model=List[user_schema.User], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = users_service.get_all(db, skip, limit)
    if users is None or len(users) < 1:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No users found!")
    return users



def get_user_by_token(token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):
    token_data = check_credentials(token)

    user = users_service.get_by_email(db, email= token_data.username)
    if user is None:
        raise credentials_exception
    if user.status == 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


@router.get("/me", response_model=user_schema.User,status_code=status.HTTP_200_OK)
def get_current_user(current_user: user_schema.User = Depends(get_user_by_token)):
    return current_user


@router.get("/{user_id}", response_model=user_schema.User, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = users_service.get_by_id(db, user_id=user_id)
    if user is None:
        raise HttpException(status_code=status.HTTP_200_OK, detail="User not found")
    return user

@router.put("/{user_id}", response_model=user_schema.User, status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, user: user_schema.UserEdit, db: Session = Depends(get_db), token: str = Depends(authentication.oauth2_scheme)):
    token_data = check_credentials(token)
    user_exists = users_service.get_by_email(db, token_data.username)
    if user_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if user_exists.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have required permissions for this action!")
    else:
        if user.old_password is None and user.password is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You need to enter your old password before entering the new one!")
        if user.password is not None and user.old_password is not None:
            psw_match = authentication.verify_password(user.old_password, user_exists.password)
            if psw_match == False:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password!")        
        edited_user = users_service.update_user(db, user, user_id)
        return edited_user


