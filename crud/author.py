from http.client import HTTPException
from database import Session
from .decorators import db_session
from sqlalchemy.orm import sessionmaker

import models
import schemas


class AuthorRepository:
    @db_session
    def find(self, author_id: int, db) -> models.Author:
        author = db.query(models.Author).where(
            models.Author.id == author_id).first()
        if author is None:
            raise HTTPException(400, 'this author could not be found')
        author.books
        return author

    @db_session
    def find_by_name(self, author_name: str, db):
        return db.query(models.Author).where(models.Author.first_name.ilike(author_name) or models.Author.last_name.ilike(author_name)).all()

    @db_session
    def list(self, limit: int, db):
        authors = db.query(models.Author).limit(limit).all()
        [author.books for author in authors]
        return authors

    @db_session
    def create(self, author: schemas.AuthorCreate):
        with Session() as db:
            new_author = models.Author(
                first_name=author.first_name,
                last_name=author.last_name
            )
            db.add(new_author)
            db.commit()
            db.refresh(new_author)
            new_author.books
            return new_author

    @db_session
    def delete(self, author_id, db):
        author = db.query(models.Author).where(
            models.Author.id == author_id).first()
        if author is None:
            return
        db.delete(author)
        db.commit()
        return author
