from typing import List, Optional
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

    def find(self, id: int) -> Optional[Author]:
        author = self.session.scalars(
            select(AuthorModel).where(AuthorModel.id == id)
        ).first()
        if author is None:
            return None
        return author

    def list(self) -> list[Author]:
        author_models = self.session.scalars(select(AuthorModel)).all()
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
        author = self.session.scalars(
            select(AuthorModel).where(AuthorModel.id == author_id)
        ).first()
        if author is None:
            return False
        self.session.delete(author)
        self.session.commit()
        return True
