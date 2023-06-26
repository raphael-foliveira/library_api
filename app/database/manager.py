from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session


class DatabaseManager:
    def __init__(self, entity_class: type, session_maker: sessionmaker[Session]):
        self.entity_class = entity_class
        self.session = session_maker

    def list(self):
        with self.session() as db:
            return db.query(self.entity_class).all()

    def find(self, id: int):
        with self.session() as db:
            object = db.query(self.entity_class).filter_by(id=id).first()
            return object

    def create(self, new_object: BaseModel):
        with self.session() as db:
            db.add(new_object)
            db.commit()
            db.refresh(new_object)
            db.flush()
            return new_object

    def delete(self, object: BaseModel):
        try:
            with self.session() as db:
                db.delete(object)
                db.commit()
                return True
        except:
            return False
