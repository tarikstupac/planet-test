from typing import Optional
from pydantic import BaseModel, constr, PositiveFloat, PositiveInt
from datetime import datetime

from schemas.user_schema import User


class Transaction(BaseModel):
    id : int
    date_created : datetime
    date_processed : datetime
    status : int
    total_price : PositiveFloat
    total_tiles : PositiveInt
    user_id : int
    user : User
    
    class Config:
        orm_mode = True