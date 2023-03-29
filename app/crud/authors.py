from app.database import DatabaseManager
from app import models, schemas
from app.database.config import engine
from sqlalchemy.engine import Engine


class AuthorRepository:
    def __init__(self, engine: Engine = engine):
        self.manager = DatabaseManager(models.Author, engine)

    def find(self, author_id: int) -> schemas.Author:
        if (author := self.manager.find(author_id)) is None:
            raise Exception("Author not found")
        return author

    def list(self) -> list[schemas.Author]:
        return self.manager.list()

    def create(self, author: schemas.AuthorCreate) -> schemas.Author:
        new_author = models.Author(
            first_name=author.first_name, last_name=author.last_name
        )
        self.manager.create(new_author)
        return new_author

    def delete(self, author_id) -> bool:
        author = self.find(author_id)
        return self.manager.delete(author)


def get_author_repository():
    return AuthorRepository()
