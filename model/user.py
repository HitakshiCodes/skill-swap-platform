from sqlalchemy import Column, Integer, String, Boolean
from app import db

class User(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    location = Column(String(100))
    availability = Column(String(100))
    is_public = Column(Boolean, default=True)

