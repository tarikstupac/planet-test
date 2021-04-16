from database import Base
from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy import DateTime, func
from sqlalchemy.orm import relationship
from models.countries import Country


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True, index=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(20), nullable=False)
    status = Column(SmallInteger, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(30))
    flag = Column(SmallInteger)
    map_style = Column(SmallInteger)
    display_name = Column(String(20))
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship("Country", backref="users")

    def __init__(self, username, email, password, status, first_name, last_name, phone, flag, map_style, display_name, country_id):
        self.username = username
        self.email = email
        self.password = password
        self.status = status
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.flag = flag
        self.map_style = map_style
        self.display_name = display_name
        self.country_id = country_id

    def __repr__(self):
            return """<User(username'{0}', email'{1}', password'{2}', status'{3}',
            first_name'{4}', last_name'{5}', phone'{6}', flag'{7}', map_style'{8}',
            display_name'{9}', country_id'{10}'>""".format(self.username, self.email,
            self.password, self.status, self.first_name, self.last_name, self.phone,
            self.flag, self.map_style, self.display_name, self.country_id)


Base.metadata.create_all()