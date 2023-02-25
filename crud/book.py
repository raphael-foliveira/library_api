from database import DatabaseManager

import models
import schemas


class BookRepository:

    def __init__(self):
        self.manager = DatabaseManager(models.Book)

    def find(self, book_id: int) -> models.Book:
        return self.manager.find(book_id)

    def list(self) -> list[models.Book]:
        return self.manager.list()

    def create(self, book: schemas.BookCreate) -> models.Book:
        new_book = models.Book(
            title=book.title,
            author_id=book.author_id,
            release_date=book.release_date,
            number_of_pages=book.number_of_pages,
            image_url=book.image_url or None
        )
        self.manager.create(new_book)
        return new_book

    def delete(self, book_id) -> models.Book:
        book = self.manager.find(book_id)
        self.manager.delete(book)
        return book
