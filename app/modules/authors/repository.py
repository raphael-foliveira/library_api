from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.interfaces.repository import Repository

from . import models, schemas


class AuthorRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    def find(self, id: int):
        if (
            author := self.session.query(models.Author).filter_by(id=id).first()
        ) is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    def list(self):
        return self.session.query(models.Author).all()

    def create(self, author: schemas.AuthorCreate):
        author_model = models.Author(
            first_name=author.first_name, last_name=author.last_name
        )
        self.session.add(author_model)
        self.session.commit()
        self.session.refresh(author_model)
        self.session.flush()
        return author_model

    def delete(self, author_id: int) -> None:
        if (
            author := self.session.query(models.Author).filter_by(id=author_id).first()
        ) is None:
            raise HTTPException(status_code=404, detail="Author not found")
        self.session.delete(author)
        self.session.commit()
