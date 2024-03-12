from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.interfaces.repository import Repository

from . import schemas
from .entities import Author
from .models import AuthorModel


class AuthorRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session)

    def create(self, author: schemas.AuthorCreate):
        author_model = AuthorModel(
            first_name=author.first_name, last_name=author.last_name
        )
        self.session.add(author_model)
        self.session.commit()
        self.session.refresh(author_model)
        self.session.flush()
        return author_model.to_entity()
