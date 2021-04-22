from sqlalchemy.orm import Session
from datetime import datetime
import csv
from database import SessionLocal, engine, get_db
from models.countries import Country
from models.users import User
from models.tiles import Tile
from models.transactions import Transaction
from models.transaction_details import TransactionDetail


session = Session(bind= engine)

def read_country_data():
    result = {}
    with open('data.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = ',', dialect='excel')

        for row in csv_reader:
            for column, value in row.items():
                result.setdefault(column, []).append(value)   
    return result
                
def seed_test_data():
    #create all countries
    result = read_country_data()
    for i in range(0,len(result['Name'])):
        country = Country(id=result['Code'][i], name=result['Name'][i], locked=0, price_multiplier=1.0)
        session.add(country)
    session.commit()
    session.close()


if __name__ == '__main__':
    print("Creating seed dataaaaaa")
    seed_test_data()
    print("Finished creating test data")
