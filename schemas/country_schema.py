from typing import Optional
from pydantic import BaseModel, constr

class Country(BaseModel):
    id: str
    name : str = constr(min_length=3, max_length=50)
    locked : int
    code : str = constr(min_length=1, max_length=10)
    price_multiplier : float


    class Config:
        orm_mode = True

