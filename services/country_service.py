from sqlalchemy.orm import Session
from models import countries
from schemas import country_schema

def get_all(db:Session, skip:int = 0, limit:int = 100):
    return db.query(countries.Country).offset(skip).limit(limit).all()

def get_by_id(db:Session, country_id: str):
    return db.query(countries.Country).filter(countries.Country.id == country_id).first()
