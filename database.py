from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
#LOCAL_DB_URL = 'postgresql+psycopg2://test1:password@localhost:5432/planetix'
conn_string = DATABASE_URL[11:]

#create Postgres db engine
engine = create_engine('postgresql+psycopg2://'+conn_string, echo=True, pool_pre_ping=True, pool_use_lifo=True)
#engine = create_engine(LOCAL_DB_URL, echo=True, pool_pre_ping=True, pool_use_lifo=True)

#declare model base
Base = declarative_base(engine)

#define session
SessionLocal = sessionmaker(autocommit=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()