from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.config import Base
from app.models import *

mock_engine = create_engine("sqlite:///:memory:")
mock_session = sessionmaker(bind=mock_engine)

Base.metadata.create_all(mock_engine)
