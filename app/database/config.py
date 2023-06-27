import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, orm

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
assert DATABASE_URL is not None

engine = create_engine(DATABASE_URL)
session = orm.sessionmaker(engine)
Base = orm.declarative_base()
