from sqlalchemy.orm import sessionmaker, Session

from app.database.config import session
from app.interfaces.repository import Repository

from . import models, schemas


class AuthorRepository(Repository):
    def __init__(self, sessionmaker: sessionmaker[Session]):
        self.session = sessionmaker

    def find(self, id: int) -> schemas.Author:
        with self.session() as db:
            if (author := db.query(models.Author).filter_by(id=id).first()) is None:
                raise Exception("Author not found")
            return author

    def list(self) -> list[schemas.Author]:
        with self.session() as db:
            return db.query(models.Author).all()

    def create(self, author: schemas.AuthorCreate) -> schemas.Author:
        author_model = models.Author(
            first_name=author.first_name,
            last_name=author.last_name
        )
        with self.session() as db:
            db.add(author_model)
            db.commit()
            db.refresh(author_model)
            db.flush()
            return author_model

    def delete(self, author_id: int) -> bool:
        with self.session() as db:
            if (author := db.query(models.Author).filter_by(id=author_id).first()) is None:
                raise Exception("Author not found")
            db.delete(author)
            db.commit()
            return True
       
