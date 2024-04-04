from sqlalchemy.orm import Session

from app.interfaces.repository import Repository

from . import schemas
from .models import AuthorModel


class AuthorRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, AuthorModel)

    def create(self, model: schemas.AuthorCreate):
        author_model = AuthorModel(
            first_name=model.first_name, last_name=model.last_name
        )
        self.session.add(author_model)
        self.session.commit()
        self.session.refresh(author_model)
        self.session.flush()
        return author_model.to_entity()
