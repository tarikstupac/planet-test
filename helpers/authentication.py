from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import SecretStr

SECRET_KEY = "396b67b31db57d4380e09cb08e5b2c435744110b3969b816a1f6e2f7b1099d42"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXIPRE_MINUTES = 2880

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    #CHANGE THIS PART AFTER TESTING
    # currently fetches plain string password from db and hashes it
    if hashed_password == 'test123':
        psw_hash = get_password_hash(hashed_password)
    else:
        psw_hash = hashed_password
    return pwd_context.verify(plain_password, psw_hash)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str = Depends(oauth2_scheme)):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    