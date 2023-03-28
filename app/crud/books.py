from app import models, schemas
from app.database import DatabaseManager
from app.database.config import engine
from sqlalchemy.engine import Engine


class BookRepository:
    def __init__(self, engine: Engine = engine):
        self.manager = DatabaseManager(models.Book, engine)

    def find(self, book_id: int) -> schemas.Book:
        if (book := self.manager.find(book_id)) is None:
            raise Exception("Book not found")
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
        self.manager.create(new_book)
        return new_book

    def delete(self, book_id) -> bool:
        book = self.find(book_id)
        return self.manager.delete(book)
