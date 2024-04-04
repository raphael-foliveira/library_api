from sqlalchemy.orm import Session
from app.interfaces.repository import Repository
from . import schemas
from .models import BookModel


class BookRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, BookModel)

    def create(self, model: schemas.CreateBook):
        new_book = BookModel(
            title=model.title,
            author_id=model.author_id,
            release_date=model.release_date,
            number_of_pages=model.number_of_pages,
            image_url=model.image_url or None,
        )
        self.session.add(new_book)
        self.session.commit()
        self.session.refresh(new_book)
        self.session.flush()
        return new_book.to_entity()
