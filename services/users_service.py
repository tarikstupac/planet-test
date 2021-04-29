from sqlalchemy.orm import Session
from sqlalchemy import func, join, desc
from sqlalchemy.sql import label
from models import users, tiles
from schemas import user_schema
from sqlalchemy.exc import SQLAlchemyError
from helpers.authentication import get_password_hash
from helpers.image_converter import save_image


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(users.User).offset(skip).limit(limit).all()

def get_by_tiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(tiles.Tile)

def get_tiles_count_by_user(db:Session, skip: int = 0, limit: int = 100):
    return db.query(tiles.Tile.user_id, users.User.username, users.User.flag, label('number_of_tiles', func.count(tiles.Tile.id))).join(users.User).\
    group_by(tiles.Tile.user_id, users.User.username, users.User.flag).order_by(func.count(tiles.Tile.id).desc()).offset(skip).limit(limit).all()

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
        profile_image=user.profile_image,
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
    
    if "profile_image" in update_data:
       # update_data["profile_image"] = save_image(user.profile_image)
       update_data["profile_image"] = 'https://thispersondoesnotexist.com/image'
        
    for key,value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def activate_user(db: Session, user_id: int):
    db_user = get_by_id(db, user_id)
    db_user.status = 1
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


    
