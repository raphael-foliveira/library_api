from sqlalchemy.orm import Session
from fastapi import Depends
from .repository import BookRepository
from app.database.config import get_db


def get_upload_path(authorId: str):
    return f"./uploads/{authorId}"


def get_books_repository(db: Session = Depends(get_db)):
    return BookRepository(db)
