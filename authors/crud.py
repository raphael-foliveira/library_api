from database import DatabaseManager

from .models import Author
from . import schemas


class AuthorRepository:
    def __init__(self):
        self.manager = DatabaseManager(Author)

    def find(self, author_id: int) -> schemas.Author:
        return self.manager.find(author_id)

    def list(self) -> list[schemas.Author]:
        return self.manager.list()

    def create(self, author: schemas.AuthorCreate) -> Author:
        new_author = Author(first_name=author.first_name, last_name=author.last_name)
        self.manager.create(new_author)
        return new_author

    def delete(self, author_id) -> Author:
        author = self.manager.find(author_id)
        self.manager.delete(author)
        return author
