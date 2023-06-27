from fastapi import Depends
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from app.database import DatabaseManager
from app.database.config import session
from app.interfaces.repository import Repository

from . import models, schemas


class AuthorRepository(Repository):
    def __init__(self, session_maker: sessionmaker[Session] = session):
        self.manager = DatabaseManager(models.Author, session_maker)

    def find(self, id: int) -> schemas.Author:
        if (author := self.manager.find(id)) is None:
            raise Exception("Author not found")
        return author

    def list(self) -> list[schemas.Author]:
        return self.manager.list()

    def create(self, model: schemas.AuthorCreate) -> schemas.Author:
        new_author = models.Author(
            first_name=model.first_name, last_name=model.last_name
        )
        self.manager.create(new_author)
        return new_author

    def delete(self, author_id: int) -> bool:
        author = self.find(author_id)
        return self.manager.delete(author)



