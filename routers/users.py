from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from jose import JWTError
from schemas import user_schema, token_schema
from services import users_service
from helpers import authentication


router = APIRouter(prefix='/users',tags=['Users'])


@router.get("/", response_model=List[user_schema.User], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = users_service.get_all(db, skip, limit)
    if users is None or len(users) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No users found!")
    return users


def get_user_by_token(token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )
    try:
        payload = authentication.decode_token(token=token)
        username: str = payload.get("sub")
        print(username)
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username = username)
        print(token_data)
    except JWTError:
        raise credentials_exception
    
    user = users_service.get_by_email(db, email= token_data.username)
    if user is None:
        raise credentials_exception
    if user.status == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    print(user)
    return user


@router.get("/me", response_model=user_schema.User,status_code=status.HTTP_200_OK)
def get_current_user(current_user: user_schema.User = Depends(get_user_by_token)):
    print("current_user")
    return current_user


@router.get("/{user_id}", response_model=user_schema.User, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = users_service.get_by_id(db, user_id=user_id)
    if user is None:
        raise HttpException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


