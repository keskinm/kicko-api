import enum

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from database.base import Base


class UserBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, unique=True)
    firebase_id = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    email = Column(String(100), unique=True)
    country = Column(String)
    zone = Column(String)
    phone_number = Column(String)
    image_id = Column(String)

    def __init__(
        self,
        firebase_id,
        username,
        password,
        email,
        image_id=None,
        country=None,
        zone=None,
        phone_number=None,
    ):
        self.firebase_id = firebase_id
        self.username = username
        self.set_password(password)
        self.email = email
        self.country = country
        self.zone = zone
        self.phone_number = phone_number
        self.image_id = image_id

    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)
