from pydantic import BaseModel
from .config import Session


class DatabaseManager:
    def __init__(self, entity_class):
        self.entity_class = entity_class

    def list(self):
        with Session() as db:
            return db.query(self.entity_class).all()

    def find(self, id: int):
        with Session() as db:
            object = db.query(self.entity_class).filter_by(id=id).first()
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
                return True
        except:
            return False
