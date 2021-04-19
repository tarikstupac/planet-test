from sqlalchemy.orm import Session
from models import users
from schemas import user_schema


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(users.User).offset(skip).limit(limit).all()

def get_by_id(db: Session, user_id: int):
    return db.query(users.User).filter(users.User.id == user_id).first()

def get_by_email(db: Session, email: str):
    return db.query(users.User).filter(users.User.email == email).first()