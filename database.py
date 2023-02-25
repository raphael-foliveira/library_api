import os
from typing import Type, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel
import pydantic
from sqlalchemy import create_engine, orm, select
import sqlalchemy


class DatabaseURLNotSetException(Exception):
    ...


load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    raise DatabaseURLNotSetException("Database URL couldn't be loaded")

engine = create_engine(DATABASE_URL)
Session = orm.sessionmaker(bind=engine)
Base = orm.declarative_base()


class DatabaseManager:

    def __init__(self, entity_class):
        self.entity_class = entity_class

    def list(self):
        with Session() as db:
            return db.query(self.entity_class).all()

    def find(self, id: int):
        with Session() as db:
            object = db.query(self.entity_class).filter_by(id=id).first()
            if (object is None):
                raise Exception("object not found")
            return object

    def create(self, new_object: BaseModel):
        try:
            with Session() as db:
                db.add(new_object)
                db.commit()
                db.refresh(new_object)
                return True
        except:
            return False

    def delete(self, object):
        try:
            with Session() as db:
                db.delete(object)
                db.commit()
                db.refresh(object)
                return True
        except:
            return False
