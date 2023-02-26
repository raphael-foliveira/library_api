from database import DatabaseManager

import models
import schemas


class BookRepository:

    def __init__(self):
        self.manager = DatabaseManager(models.Book)

    def find(self, book_id: int) -> schemas.Book:
        return self.manager.find(book_id)

    def list(self) -> list[schemas.Book]:
        return self.manager.list()

    def create(self, book: schemas.BookCreate) -> schemas.Book:
        new_book = models.Book(
            title=book.title,
            author_id=book.author_id,
            release_date=book.release_date,
            number_of_pages=book.number_of_pages,
            image_url=book.image_url or None
        )
        if self.manager.create(new_book):
            return new_book
        raise

    def delete(self, book_id) -> schemas.Book:
        book = self.manager.find(book_id)
        if self.manager.delete(book):
            return book
        raise
