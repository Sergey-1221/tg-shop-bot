from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    #tg_id = #ID пользоваетеля из телеграма 


if __name__ == "__main__":
    engine = create_engine('sqlite:///store.db')
    Base.metadata.create_all(engine)