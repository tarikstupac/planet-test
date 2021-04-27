from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError
from helpers.authentication import oauth2_scheme, verify_password, ACCESS_TOKEN_EXIPRE_MINUTES, create_access_token
from helpers.authentication import get_password_hash, create_refresh_token, verify_token, decode_refresh_token, decode_token
from database import get_db
from services import users_service
from schemas import token_schema, user_schema

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
    refresh_token = create_refresh_token(data={"sub":user_exists.email})
    
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
    

@router.post('/register', response_model=token_schema.Token, status_code=status.HTTP_201_CREATED)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user_exists = users_service.get_by_email(db, user.email)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="There is already an account tied to this e-mail!")
    if user_exists is not None and user_exists.username == user.username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="There is already an account with this username!")
    else:
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        user_db = users_service.insert_user(db,user)
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong while creating the user!")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXIPRE_MINUTES)
        access_token = create_access_token(data={"sub":user.email}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data={"sub":user.email})
        return {"access_token": access_token, "token_type":"bearer", "refresh_token": refresh_token}

@router.post('/refresh', response_model=token_schema.Token, status_code=status.HTTP_200_OK)
def refresh_token(token: token_schema.Token, db: Session = Depends(get_db)):
    valid = verify_token(token.access_token)
    if valid:
        try:
            payload = decode_token(token=token.access_token)
            username: str = payload.get("sub")
        except:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong while decoding token")
        user = users_service.get_by_email(db, username)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXIPRE_MINUTES)
        access_token = create_access_token(data={"sub":user.email}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type":"bearer", "refresh_token":token.refresh_token}
    else:
        try:
            payload = decode_refresh_token(token=token.refresh_token)
            username: str = payload.get("sub")
        except:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong while decoding token")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials.")
        user = users_service.get_by_email(db, username)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXIPRE_MINUTES)
        access_token = create_access_token(data={"sub":user.email}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": token.refresh_token}


@router.post('/forgotpassword', status_code=status.HTTP_200_OK, response_description="Reset link was sent to the entered e-mail.")
def forgot_password(forgot_password: user_schema.UserForgotPassword , db: Session = Depends(get_db)):
    user_exists = users_service.get_by_email(db, forgot_password.email)
    if user_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is no account tied to this email!")
    else:
        return {"detail":"Reset link was sent to the entered e-mail."}
        
def check_credentials(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )
    try:
        payload = decode_token(token=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username = username)
        return token_data
    except JWTError:
        raise credentials_exception  
    

