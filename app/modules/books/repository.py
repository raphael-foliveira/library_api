from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session


from . import schemas
from .models import BookModel
from .entities import Book


class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def find(self, id: int) -> Book:
        statement = select(BookModel).where(BookModel.id == id)
        book: Optional[BookModel] = self.session.scalars(statement).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book.to_entity()

    def list(self):
        statement = select(BookModel)
        books = self.session.scalars(statement).all()
        return [book.to_entity() for book in books]

    def create(self, book: schemas.BookCreate):
        new_book = BookModel(
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
        return new_book.to_entity()

    def delete(self, book_id: int) -> bool:
        statement = select(BookModel).where(BookModel.id == book_id)
        book = self.session.scalars(statement).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        self.session.delete(book)
        self.session.commit()
        return True
