from fastapi import HTTPException
from database import DatabaseManager

from . import models, schemas


class AuthorRepository:
    def __init__(self):
        self.manager = DatabaseManager(models.Author)

    def find(self, author_id: int) -> schemas.Author:
        try:
            return self.manager.find(author_id)
        except:
            raise HTTPException(status_code=404, detail="Author not found")

    def list(self) -> list[schemas.Author]:
        return self.manager.list()

    def create(self, author: schemas.AuthorCreate) -> schemas.Author:
        try:
            new_author = models.Author(
                first_name=author.first_name, last_name=author.last_name
            )
            self.manager.create(new_author)
            return new_author
        except:
            raise HTTPException(status_code=400, detail="Author could not be created")

    def delete(self, author_id) -> schemas.Author:
        author = self.manager.find(author_id)
        self.manager.delete(author)
        return author
