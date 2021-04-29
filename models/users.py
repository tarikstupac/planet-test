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
    password = Column(String(100), nullable=False)
    status = Column(SmallInteger, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(30), nullable=True)
    flag = Column(String(10), nullable=True)
    map_style = Column(SmallInteger)
    profile_image = Column(String(150), nullable=True)
    country_id = Column(String, ForeignKey('countries.id'), nullable=False)
    country = relationship("Country", backref="users")

    def __init__(self, username: str, email: str, password: str, status: int, first_name: str, last_name: str, phone: str, flag: int, map_style: int, profile_image: str, country_id: str):
        self.username = username
        self.email = email
        self.password = password
        self.status = status
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.flag = flag
        self.map_style = map_style
        self.profile_image = profile_image
        self.country_id = country_id

    def __repr__(self):
        return """<User(username'{0}', email'{1}', password'{2}', status'{3}',
            first_name'{4}', last_name'{5}', phone'{6}', flag'{7}', map_style'{8}',
            profile_image'{9}', country_id'{10}'>
            """.format(self.username, self.email,
                       self.password, self.status, self.first_name, self.last_name, self.phone,
                       self.flag, self.map_style, self.profile_image, self.country_id)

