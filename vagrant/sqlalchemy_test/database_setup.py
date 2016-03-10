import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    # columnNmae = Column(attributes, ...)
    # example attributes:
    # String(250), Integer, relationship(Class), nullable=False,
    # primary_key=True, ForeignKey('some_table.id')

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant = relationship(Restaurant)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    @property
    def serialize(self):
        """Returns object data in easily serializeable format
		"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


#### insert at end of file ####

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
