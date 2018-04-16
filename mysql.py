"""
Creates similar structures to MongoDB. Not in use, just a demo
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    age = Column(int)
    birthday = Column(Date)
    public = Column(Boolean, nullable=False)
