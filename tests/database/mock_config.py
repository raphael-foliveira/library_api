import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
assert TEST_DATABASE_URL is not None


mock_engine = create_engine(TEST_DATABASE_URL)
mock_sessionmaker = sessionmaker(bind=mock_engine)
