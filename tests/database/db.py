import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
assert TEST_DATABASE_URL is not None

engine_test = create_engine(TEST_DATABASE_URL)
sessionmaker_test = sessionmaker(bind=engine_test)


def get_test_db():
    db = sessionmaker_test()
    try:
        yield db
    finally:
        db.close()
