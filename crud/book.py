from crud.decorators import db_session
from database import Session

import models
import schemas


class BookRepository:
    @db_session
    def find(self, book_id: int, db):
        return db.query(models.Book).filter(models.Book.id == book_id).first()

    @db_session
    def list(self, db, limit: int = 100):
        books = db.query(models.Book).limit(limit).all()
        [book.author for book in books]
        return books

    @db_session
    def retrieve_by_title(self, book_title: str, db):
        return db.query(models.Book).filter(models.Book.title == book_title).all()

    @db_session
    def create(self, book: schemas.BookCreate, db):
        new_book = models.Book(
            title=book.title,
            author_id=book.author_id,
            release_date=book.release_date,
            number_of_pages=book.number_of_pages,
            image_url=book.image_url or None
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book

    @db_session
    def delete(self, book_id, db):
        book = db.query(models.Book).filter(
            models.Book.id == book_id).first()
        if book is None:
            return
        db.delete(book)
        db.commit()
        return book
