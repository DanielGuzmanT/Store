from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"

    id   = Column(Integer, primary_key=True)
    code = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String(250))
    price_unit  = Column(Integer)
    price_pack  = Column(Integer)


class User(Base):
    __tablename__ = "user"

    id       = Column(Integer, primary_key=True)
    email    = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)


# Creating database
# if __name__ == '__main__':
# engine = create_engine('sqlite:///lucas_store.db')
# Base.metadata.create_all(engine)
