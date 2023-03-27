import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, orm

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
assert DATABASE_URL is not None

engine = create_engine(DATABASE_URL)
Session = orm.sessionmaker(bind=engine)
Base = orm.declarative_base()
