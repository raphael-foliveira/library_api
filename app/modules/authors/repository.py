from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.interfaces.repository import Repository

from . import schemas
from .models import AuthorModel
from .entities import Author


class AuthorRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    def find(self, id: int) -> Author:
        statement = select(AuthorModel).where(AuthorModel.id == id)
        author = self.session.scalars(statement).first()
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    def list(self):
        statement = select(AuthorModel)
        author_models = self.session.scalars(statement).all()
        return [author.to_entity() for author in author_models]

    def create(self, author: schemas.AuthorCreate):
        author_model = AuthorModel(
            first_name=author.first_name, last_name=author.last_name
        )
        self.session.add(author_model)
        self.session.commit()
        self.session.refresh(author_model)
        self.session.flush()
        return author_model.to_entity()

    def delete(self, author_id: int) -> bool:
        statement = select(AuthorModel).where(AuthorModel.id == author_id)
        author = self.session.scalars(statement).first()
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        self.session.delete(author)
        self.session.commit()
        return True
