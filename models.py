from sqlalchemy import Table, Index, Integer, BigInteger, String, Float, Column, Text, \
                       DateTime, Boolean, PrimaryKeyConstraint, \
                       UniqueConstraint, ForeignKeyConstraint, ForeignKey

from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import  create_engine
import time


Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)


class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True)#ID пользоваетеля из телеграма 
    role = Column(String(100), nullable=False)
    


if __name__ == "__main__":
    engine = create_engine('sqlite:///store.db')
    Base.metadata.create_all(engine)