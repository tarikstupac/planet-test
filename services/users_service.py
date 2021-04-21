from sqlalchemy.orm import Session
from models import users
from schemas import user_schema
from sqlalchemy.exc import SQLAlchemyError
from helpers.authentication import get_password_hash


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(users.User).offset(skip).limit(limit).all()

def get_by_id(db: Session, user_id: int):
    return db.query(users.User).filter(users.User.id == user_id).first()

def get_by_email(db: Session, email: str):
    return db.query(users.User).filter(users.User.email == email).first()

def insert_user(db:Session, user: user_schema.UserCreate):
    db_user = users.User(
        username=user.username,
        email=user.email,
        password=user.password,
        status=user.status,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        flag=user.flag,
        map_style=user.map_style,
        display_name=user.display_name,
        country_id=user.country_id
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        return None

def update_user(db: Session, user: user_schema.UserEdit, user_id:int):
    db_user = get_by_id(db, user_id)
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = get_password_hash(user.password)
    
    for key,value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

    
