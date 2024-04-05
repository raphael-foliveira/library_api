from sqlalchemy.orm import sessionmaker
from app.interfaces.repository import Repository
from . import schemas
from .models import BookModel


class BookRepository(Repository):
    def __init__(self, session: sessionmaker):
        super().__init__(session, BookModel)

    def create(self, model: schemas.CreateBook):
        with self.session() as db:
            new_book = BookModel(
                title=model.title,
                author_id=model.author_id,
                release_date=model.release_date,
                number_of_pages=model.number_of_pages,
                image_url=model.image_url or None,
            )
            db.add(new_book)
            db.commit()
            return new_book.to_entity()
