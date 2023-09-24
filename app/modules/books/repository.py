from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def find(self, id: int) -> models.Book:
        book = self.session.scalars(
            select(models.Book).where(models.Book.id == id)
        ).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def list(self):
        return self.session.scalars(select(models.Book)).all()

    def create(self, book: schemas.BookCreate):
        new_book = models.Book(
            title=book.title,
            author_id=book.author_id,
            release_date=book.release_date,
            number_of_pages=book.number_of_pages,
            image_url=book.image_url or None,
        )
        self.session.add(new_book)
        self.session.commit()
        self.session.refresh(new_book)
        self.session.flush()
        return new_book

    def delete(self, book_id: int) -> bool:
        book = self.session.scalars(
            select(models.Book).where(models.Book.id == book_id)
        ).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        self.session.delete(book)
        self.session.commit()
        return True
