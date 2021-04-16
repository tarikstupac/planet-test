from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal, engine, get_db
from models.countries import Country
from models.users import User
from models.tiles import Tile
from models.transactions import Transaction
from models.transaction_details import TransactionDetail


session = Session(bind= engine)

def seed_test_data():
    #create a few countries
    usa = Country("United States of America", 0, "US", 1.0)
    mexico = Country("Mexico", 0, "MEX", 1.0)
    canada = Country("Canada", 0, "CA", 1.0)

    session.add(usa)
    session.add(mexico)
    session.add(canada)
    session.commit()

#create a few users
    user1 = User("test1", "test1@test.com", "test123", 1, "Test", "Testovic", "+38762000000", 1, 1, "Testoo", usa.id)
    user2 = User("test2", "test2@test.com", "test123", 2, "Teston", "Testony", "+38565123123", 1, 1, "Testorony", canada.id)

    session.add(user1)
    session.add(user2)
    session.commit()

#create a few tiles
    tile1 = Tile("023113001230003213130", 100.0, "Somewhere, Someplace, USA", 0, 1, 0, datetime.utcnow(), usa.id, user1.id)
    tile2 = Tile("023113001230003213132", 100.0, "Somewhere, Someplace, USA", 0, 1, 0, datetime.utcnow(), usa.id, user1.id)
    tile3 = Tile("023113001230003213131", 100.0, "Somewhere, Someplace, USA", 0, 1, 0, datetime.utcnow(), usa.id, user1.id)
    tile4 = Tile("023113001230003302020", 100.0, "Somewhere, Someplace, USA", 0, 1, 0, datetime.utcnow(), usa.id, user1.id)

    session.add(tile1)
    session.add(tile2)
    session.add(tile3)
    session.add(tile4)
    session.commit()
    session.close()