from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from engine.engine import MAIN_ENGINE

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    firebase_id = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
    email = Column(String(100), unique=True)
    country = Column(String)
    zone = Column(String)
    phone_number = Column(String)

    def __init__(
        self,
        firebase_id,
        username,
        password,
        email,
        country=None,
        zone=None,
        phone_number=None,
    ):
        self.firebase_id = firebase_id
        self.username = username
        self.password = password
        self.email = email
        self.country = country
        self.zone = zone
        self.phone_number = phone_number


Base.metadata.create_all(MAIN_ENGINE)

#
# from sqlalchemy.orm import sessionmaker
#
# Session = sessionmaker(bind=MAIN_ENGINE)
# session = Session()
#
# User.__table__.drop(MAIN_ENGINE)
# r = list(session.query(User).filter())
# r
#
# session.add(User("1234", "Mustafa_Keskin", "python", "mouss42490@gmail.com", "France", "loire", "+33782425371"))
# session.add(User(firebase_id="1234", username="Mustafa_Keskin", password="python", email="mouss42490@gmail.com"))
#
# session.commit()
# from queries.queries import Queries
# r = Queries().get(User)
# r
