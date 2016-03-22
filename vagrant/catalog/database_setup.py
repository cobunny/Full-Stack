from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.dialects.drizzle import TIMESTAMP

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format for Jsonify"""
        return {
            'id': self.id,
            'name': self.name,
        }


class CategoryItem(Base):
    __tablename__ = 'category_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    lastTime = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format for Jsonify"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,

        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
