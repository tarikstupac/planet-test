"""A module containing the necessary code for the SQLAlchemy Users model"""
from database import Base
from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy import DateTime, func
from sqlalchemy.orm import relationship
from models.countries import Country


class User(Base):
    """An SQLAlchemy class representing a user.
    It extends the SQLAlchemy Base model class and represents
    a table that will be generated in a database.

    :param Base: Base SQLAlchemy model
    :type Base: Base
    :param __tablename__: Defines tablename that will be used in db
    :type __tablename__: str
    :param id: Unique identifier for the user
    :type id: int
    :param username: Username of the user, must be unique
    :type username: str
    :param email: Email of the user, must be unique
    :type email: str
    :param password: Represents the password of the user in hashed format using bcrypt
    :type password: str
    :param status: A small int representing whether the status of the user (0 for inactive,1 active etc)
    :type status: int
    :param first_name: First name of the user
    :type first_name: str
    :param last_name: Last name of the user
    :type last_name: str
    :param phone: User's phone number, must be in valid format
    :type phone: str, optional
    :param flag: A string representation of the user's display flag that will be shown on map
    :type flag: str, optional
    :param map_style: The users default map style setting in small int format
    :type map_style: int
    :param profile_image: A string representing the link to the users profile image
    :type profile_image: str, optional
    :param country_id: A foreign key tied to the country table, represents user's country of origin
    :type country_id: str
    """
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
    credit = Column(Integer)
    country_id = Column(String, ForeignKey('countries.id'), nullable=False)
    country = relationship("Country", backref="users")

    def __init__(self, username: str, email: str, password: str, status: int, first_name: str, last_name: str, phone: str, flag: int, map_style: int, profile_image: str, credit: int, country_id: str):
        """Constructor method for User."""
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
        self.credit = credit
        self.country_id = country_id

    def __repr__(self):
        """String representation of the class for dev purposes

        :return: returns a formatted string in a dev friendly format
        :rtype: str
        """
        return """<User(username'{0}', email'{1}', password'{2}', status'{3}',
            first_name'{4}', last_name'{5}', phone'{6}', flag'{7}', map_style'{8}',
            profile_image'{9}', credit'{10}' country_id'{11}'>
            """.format(self.username, self.email,
                       self.password, self.status, self.first_name, self.last_name, self.phone,
                       self.flag, self.map_style, self.profile_image, self.credit, self.country_id)
