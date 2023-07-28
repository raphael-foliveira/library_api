from sqlalchemy.orm import Session

from . import models, schemas


class BookRepository:
    def __init__(self, sessionmaker: Session):
        self.session = sessionmaker

    def find(self, id: int) -> schemas.Book:
        if (book := self.session.query(models.Book).filter_by(id=id).first()) is None:
            raise Exception("Book not found")
        return book

    def list(self) -> list[schemas.Book]:
        return self.session.query(models.Book).all()

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
        if (
            book := self.session.query(models.Book).filter_by(id=book_id).first()
        ) is None:
            raise Exception("Book not found")
        self.session.delete(book)
        self.session.commit()
        return True
