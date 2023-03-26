import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, orm


class DatabaseURLNotSetException(Exception):
    ...


load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    raise DatabaseURLNotSetException("Database URL couldn't be loaded")

engine = create_engine(DATABASE_URL)
Session = orm.sessionmaker(bind=engine)
Base = orm.declarative_base()