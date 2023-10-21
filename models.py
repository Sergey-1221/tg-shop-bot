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
    descriptions = Column(String(500))

    basket = relationship("Basket", backref="basket")


class Users(Base):
    __tablename__ = 'users'
    tg_id = Column(BigInteger, primary_key=True, index=True)#ID пользоваетеля из телеграма 
    role = Column(String(100), nullable=False)#Роль admin/user 

    basket = relationship("Basket", backref="basket")

class Basket(Base):
    __tablename__ = 'basket'
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'))
    users = relationship("Users", backref="users")

    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", backref="products")



    




if __name__ == "__main__":
    engine = create_engine('sqlite:///store.db')
    Base.metadata.create_all(engine)