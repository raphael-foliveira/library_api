import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase


load_dotenv()


class Base(DeclarativeBase):
    pass


engine = create_engine(str(os.getenv("DATABASE_URL")))
session = sessionmaker(bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
