from sqlalchemy import Column, Integer, String

from tables.user.user import UserBase


class Professional(UserBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    firebase_id = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String(100), unique=True)
    country = Column(String)
    zone = Column(String)
    phone_number = Column(String)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
