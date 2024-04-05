from sqlalchemy.orm import sessionmaker

from app.interfaces.repository import Repository

from . import schemas
from .models import AuthorModel


class AuthorRepository(Repository):
    def __init__(self, session: sessionmaker):
        super().__init__(session, AuthorModel)

    def create(self, model: schemas.AuthorCreate):
        with self.session() as db:
            author_model = AuthorModel(
                first_name=model.first_name, last_name=model.last_name
            )
            db.add(author_model)
            db.commit()
            return author_model.to_entity()
