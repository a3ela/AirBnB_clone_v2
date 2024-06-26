#!/usr/bin/python3
"""This is the state class"""
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
        __tablename__: name for db table
        cities: relation with city
    """
    __tablename__ = 'states'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete',
                              backref='state')
    else:
        @property
        def cities(self):
            """Returns the list of City instances with
            state_id equals to the current State.id
            city_list: list of cities from a state
            """
            city_list = []

            for key, value in models.storage.all(State):
                    if value.state_id == self.id:
                        city_list[key] = value
            return city_list
