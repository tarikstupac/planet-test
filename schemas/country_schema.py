from typing import Optional
from pydantic import BaseModel, constr

class Country(BaseModel):
    id: str
    name : constr(min_length=3, max_length=150)
    locked : int
    price_multiplier : float


    class Config:
        orm_mode = True

