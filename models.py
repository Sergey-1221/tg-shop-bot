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
    #descriptions = Column(String(500))
    image = Column(String(255))
    basket = relationship("Basket", backref="products")


class Users(Base):
    __tablename__ = 'users'
    tg_id = Column(BigInteger, primary_key=True, index=True)#ID пользоваетеля из телеграма 
    role = Column(String(100), nullable=False, default="user")#Роль admin/user 
    balance = Column(Float, default=0.0)
    basket = relationship("Basket", backref="users")

class Basket(Base):
    __tablename__ = 'basket'
    id = Column(Integer, primary_key=True)
    users_id = Column(BigInteger, ForeignKey('users.tg_id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    status = Column(String(100),  default="0") 


    
if __name__ == "__main__":
    engine = create_engine('sqlite:///store.db')
    Base.metadata.create_all(engine)