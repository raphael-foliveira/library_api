from database import DatabaseManager

import models
import schemas


class AuthorRepository:

    def __init__(self):
        self.manager = DatabaseManager(models.Author)

    def find(self, author_id: int):
        return self.manager.find(author_id)

    def list(self, limit: int):
        return self.manager.list()

    def create(self, author: schemas.AuthorCreate):
        new_author = models.Author(
            first_name=author.first_name,
            last_name=author.last_name
        )
        self.manager.create(new_author)
        return new_author

    def delete(self, author_id):
        author = self.manager.find(author_id)
        self.manager.delete(author)
        return author
