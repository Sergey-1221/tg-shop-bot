Base = declarative_base(bind=engine)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)

'''
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer)
    balance = Column(Float)
    is_admin = Column(Boolean)

class Adminpasswords(Base):
    __tablename__ = 'passwords'
    id = Column(Integer)
    password = Column(String)
'''




if __name__ == "__main__":
    Base.metadata.create_all()