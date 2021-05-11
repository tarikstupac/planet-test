from datetime import datetime, timedelta
from os import stat
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from helpers.authentication import oauth2_scheme, verify_password, ACCESS_TOKEN_EXIPRE_MINUTES, create_access_token
from helpers.authentication import get_password_hash, create_refresh_token, verify_token, decode_refresh_token, decode_token
from database import get_db
from jose import JWTError
from services import users_service
from schemas import token_schema, user_schema
from helpers import email_sender
from redis_conf import token_watcher as r

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
    #add key to redis token watcher
    r.setex(f'{user_exists.id}_access_token', timedelta(ACCESS_TOKEN_EXIPRE_MINUTES), access_token)

    refresh_token = create_refresh_token(data={"sub":user_exists.email})
    #add refresh token key to redis token_watcher
    r.set(f'{user_exists.id}_refresh_token', refresh_token)
    
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
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
         detail="The passwords do not match!")
    else:
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        user_db = users_service.insert_user(db,user)
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong while creating the user!")

        #replace this logic with account activation email in the future.
        #Use activation_email fonction in email_sender.py and same logic from forgot password
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXIPRE_MINUTES)
        access_token = create_access_token(data={"sub":user_db.email}, expires_delta=access_token_expires)
        #add key to redis token_watcher
        r.setex(f'{user_db.id}_access_token', timedelta(ACCESS_TOKEN_EXIPRE_MINUTES), access_token)
        refresh_token = create_refresh_token(data={"sub":user_db.email})
        #add refresh token key to redis token_watcher
        r.set(f'{user_db.id}_refresh_token', refresh_token)
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
        #blacklist the old token
        r.expire(f'{user.id}_access_token', timedelta(seconds=0))

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXIPRE_MINUTES)
        access_token = create_access_token(data={"sub":user.email}, expires_delta=access_token_expires)
        #add the new token to token watcher
        r.setex(f'{user.id}_access_token', access_token_expires, access_token)
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

        r.expire(f'{user.id}_access_token', timedelta(seconds=0))

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXIPRE_MINUTES)
        access_token = create_access_token(data={"sub":user.email}, expires_delta=access_token_expires)
        #add new token to token watcher
        r.setex(f'{user.id}_access_token', access_token_expires, access_token)

        return {"access_token": access_token, "token_type": "bearer", "refresh_token": token.refresh_token}


@router.post('/forgotpassword', status_code=status.HTTP_200_OK, response_description="Reset link was sent to the entered e-mail.")
async def forgot_password(forgot_password: user_schema.UserForgotPassword , db: Session = Depends(get_db)):
    user_exists = users_service.get_by_email(db, forgot_password.email)
    if user_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is no account tied to this email!")
    else:
        password_reset_token_expires = timedelta(minutes=60)
        password_reset_token = create_access_token(data={"sub":forgot_password.email}, expires_delta=password_reset_token_expires)

        r.setex(f'{user_exists.id}_password_token', password_reset_token_expires, password_reset_token)
        await email_sender.compose_email(forgot_password, password_reset_token)
        return {"detail":"Reset link was sent to the entered e-mail."}
        

@router.post('/changepassword/', status_code=status.HTTP_202_ACCEPTED, response_description="Successfully reset password!")
def reset_password(request: user_schema.UserPasswordReset, db: Session = Depends(get_db)):
    valid = verify_token(request.confirmation)
    if valid:
        try:
            payload = decode_token(token=request.confirmation)
            username: str = payload.get("sub")
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong while decoding token")

    user_exists = users_service.get_by_email(db, username)

    if user_exists is None: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist!")

    #check for token in redis cache
    if r.exists(f'{user_exists.id}_password_token') != 0:
        redis_token = r.get(f'{user_exists.id}_password_token')
        if redis_token.decode('utf-8') != request.confirmation:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid password reset link!")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password reset link!")
    if request.password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't match!")
    user = user_schema.UserEdit(password=request.password)
    users_service.update_user(db, user, user_exists.id)
    #INVALIDATE TOKEN using redis caching
    r.expire(f'{user_exists.id}_password_token', timedelta(seconds=0))
    return {"detail":"Password successfully changed, you will be redirected to the login page shortly."}

    
@router.post('/verifyaccount', status_code=status.HTTP_200_OK, response_description="Account successfully verified")
def verify_account(request: user_schema.UserActivateAccount, db: Session = Depends(get_db)):
    valid = verify_token(request.confirmation)
    if valid:
        try:
            payload = decode_token(token=request.confirmation)
            username: str = payload.get("sub")
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong while decoding token")
    user_exists = users_service.get_by_email(db, username)
    if user_exists is None: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist!")
    
    user = users_service.activate_user(db, user_exists.id)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXIPRE_MINUTES)
    access_token = create_access_token(data={"sub":user.email}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub":user.email})
    return {"access_token": access_token, "token_type":"bearer", "refresh_token": refresh_token}

@router.post("/logout", status_code= status.HTTP_200_OK, response_description="Successfully logged out")
def logout(token: token_schema.Token, db: Session = Depends(get_db)):
    valid = verify_token(token.access_token)
    if valid:
        try:
            payload = decode_token(token=token.access_token)
            username: str = payload.get("sub")
        except:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong while decoding token")       
        user = users_service.get_by_email(db, username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the email doesn't exist.")
        #expire the token
        r.expire(f'{user.id}_access_token', timedelta(seconds=0))
        r.expire(f'{user.id}_refresh_token', timedelta(seconds=0))


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
    

