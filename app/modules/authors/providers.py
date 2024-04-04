from sqlalchemy.orm import Session
from fastapi import Depends
from .repository import AuthorRepository
from ...database.config import get_db


def get_author_repository(db: Session = Depends(get_db)):
    return AuthorRepository(db)
