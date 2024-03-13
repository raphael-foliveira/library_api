from sqlalchemy.orm import Session
from app.interfaces.repository import Repository
from . import schemas
from .models import BookModel


class BookRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session)

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
