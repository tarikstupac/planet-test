from typing import Optional
from pydantic import BaseModel, constr, EmailStr, SecretStr
from schemas.country_schema import Country

class User(BaseModel):
    id : int
    username : str = constr(min_length=3, max_length=20)
    email : EmailStr
    password : SecretStr = constr(min_length=8, max_length=20)
    status : int
    first_name : str = constr(min_length=1, max_length=50)
    last_name : str = constr (min_length=1, max_length=50)
    phone : str = constr(regex='^\+(?:[0-9] ?){6,14}[0-9]$')
    flag : Optional[int]
    map_style : Optional[int]
    display_name : str = constr(min_length=1, max_length=20)
    country_id : int 
    country : Country

    class Config:
        orm_mode = True

