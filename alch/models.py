""" models """
from sqlalchemy import Column, Integer, String
from alch.db import Base


class User(Base):
    """ user entity """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
