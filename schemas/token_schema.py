from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type : str = "bearer"
    refresh_token: Optional[str]


class TokenData(BaseModel):
    username: Optional[str] = None