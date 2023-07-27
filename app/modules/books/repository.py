from sqlalchemy.orm import sessionmaker, Session

from . import models, schemas


class BookRepository:
    def __init__(self, sessionmaker: sessionmaker[Session]):
        self.session = sessionmaker

    def find(self, id: int) -> schemas.Book:
        with self.session() as db:
            if (book := db.query(models.Book).filter_by(id=id).first()) is None:
                raise Exception("Book not found")
            return book

    def list(self) -> list[schemas.Book]:
        with self.session() as db:
            return db.query(models.Book).all()

    def create(self, book: schemas.BookCreate):
        new_book = models.Book(
            title=book.title,
            author_id=book.author_id,
            release_date=book.release_date,
            number_of_pages=book.number_of_pages,
            image_url=book.image_url or None,
        )
        with self.session() as db:
            db.add(new_book)
            db.commit()
            db.refresh(new_book)
            db.flush()
            return new_book 

    def delete(self, book_id: int) -> bool:
        with self.session() as db:
            if (book := db.query(models.Book).filter_by(id=book_id).first()) is None:
                raise Exception("Book not found")
            db.delete(book)
            db.commit()
            return True

