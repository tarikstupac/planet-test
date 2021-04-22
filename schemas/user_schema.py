from typing import Optional
from pydantic import BaseModel, constr, EmailStr, SecretStr
from schemas.country_schema import Country

class User(BaseModel):
    id : int
    username: constr(min_length=3, max_length=20)
    email : EmailStr
    status : int
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    phone: constr(regex='^\+(?:[0-9] ?){6,14}[0-9]$')
    flag : Optional[int]
    map_style : Optional[int]
    display_name: constr(min_length=1, max_length=20)
    country_id : str 
    country : Country

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=20)
    email : EmailStr
    password : constr(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
    status : int = 1
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    phone: Optional[constr(regex='^\+(?:[0-9] ?){6,14}[0-9]$')]
    flag : Optional[int]
    map_style : Optional[int]
    display_name: Optional[constr(min_length=1, max_length=20)]
    country_id : str 

    class Config:
        orm_mode = True


class UserEdit(BaseModel):
    old_password: Optional[constr(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")]
    password : Optional[constr(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")]
    first_name: Optional[constr(min_length=1, max_length=50)]
    last_name: Optional[constr(min_length=1, max_length=50)]
    phone: Optional[constr(regex='^\+(?:[0-9] ?){6,14}[0-9]$')]
    flag : Optional[int]
    map_style : Optional[int]
    display_name: Optional[constr(min_length=1, max_length=20)]
    country_id : Optional[str] 

    class Config:
        orm_mode = True

