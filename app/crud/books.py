from fastapi import HTTPException
from fastapi import Response
from app.database import DatabaseManager
from app import models, schemas


class BookRepository:
    def __init__(self):
        self.manager = DatabaseManager(models.Book)

    def find(self, book_id: int) -> schemas.Book:
        if (book := self.manager.find(book_id)) is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def list(self) -> list[schemas.Book]:
        return self.manager.list()

    def create(self, book: schemas.BookCreate) -> schemas.Book:
        new_book = models.Book(
            title=book.title,
            author_id=book.author_id,
            release_date=book.release_date,
            number_of_pages=book.number_of_pages,
            image_url=book.image_url or None,
        )
        if self.manager.create(new_book):
            return new_book
        raise

    def delete(self, book_id) -> bool:
        book = self.manager.find(book_id)
        return self.manager.delete(book)
