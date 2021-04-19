from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from helpers.authentication import oauth2_scheme, verify_password, ACCESS_TOKEN_EXIPRE_MINUTES, create_access_token
from database import get_db
from services import users_service
from schemas import token_schema

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=token_schema.Token, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_exists = users_service.get_by_email(db, form_data.username)
    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(form_data.password, user_exists.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXIPRE_MINUTES)
    access_token = create_access_token(data={"sub": user_exists.email}, expires_delta= access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

