Base = declarative_base(bind=engine)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)

if __name__ == "__main__":
    Base.metadata.create_all()