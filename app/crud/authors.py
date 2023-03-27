from fastapi import HTTPException
from app.database import DatabaseManager
from app import models, schemas


class AuthorRepository:
    def __init__(self):
        self.manager = DatabaseManager(models.Author)

    def find(self, author_id: int) -> schemas.Author:
        if (author := self.manager.find(author_id)) is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

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

    def delete(self, author_id) -> bool:
        author = self.manager.find(author_id)
        return self.manager.delete(author)
