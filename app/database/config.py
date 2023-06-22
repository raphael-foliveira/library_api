import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, orm

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
assert DATABASE_URL is not None
environment = os.getenv("ENV", "")

engine = create_engine(
    DATABASE_URL if environment != "testing" else "sqlite:///:memory:"
)
Base = orm.declarative_base()
