from typing import Optional
from pydantic import BaseModel, constr, EmailStr
from schemas.country_schema import Country


class User(BaseModel):
    id: int
    username: constr(min_length=3, max_length=20)
    email: EmailStr
    status: int
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    phone: Optional[constr(regex='^\+(?:[0-9] ?){6,14}[0-9]$')]
    flag: Optional[str]
    map_style: Optional[int]
    profile_image: Optional[constr(min_length=1, max_length=150)]
    credit: int
    country_id: str
    country: Country

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=20)
    email: EmailStr
    password: constr(
        regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
    confirm_password: constr(
        regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
    status: int = 1
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    phone: Optional[constr(regex='^\+(?:[0-9] ?){6,14}[0-9]$')]
    flag: Optional[str] = 'BA'
    map_style: Optional[int]
    profile_image: Optional[constr(min_length=1, max_length=150)] = "https://thispersondoesnotexist.com/image"
    credit: Optional[int] = 0
    country_id: str

    class Config:
        orm_mode = True


class UserEdit(BaseModel):
    old_password: Optional[constr(
        regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")]
    password: Optional[constr(
        regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")]
    first_name: Optional[constr(min_length=1, max_length=50)]
    last_name: Optional[constr(min_length=1, max_length=50)]
    phone: Optional[constr(regex='^\+(?:[0-9] ?){6,14}[0-9]$')]
    flag: Optional[str]
    map_style: Optional[int]
    profile_image: Optional[constr(min_length=1)]
    credit: Optional[int]
    country_id: Optional[str]

    class Config:
        orm_mode = True


class UserForgotPassword(BaseModel):
    email: EmailStr


class UserPasswordReset(BaseModel):
    confirmation: str
    password: constr(
        regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
    confirm_password: constr(
        regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")


class UserActivateAccount(BaseModel):
    email: EmailStr
