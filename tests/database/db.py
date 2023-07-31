import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

with open("./config_test.json") as f:
    TEST_DATABASE_URL = json.load(f)["test_database"]
    print(TEST_DATABASE_URL)

engine_test = create_engine(TEST_DATABASE_URL)
sessionmaker_test = sessionmaker(bind=engine_test)


def get_test_db():
    db = sessionmaker_test()
    try:
        yield db
    finally:
        db.close()
