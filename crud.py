from http.client import HTTPException
from database import Session

import models
import schemas


def db_session(func):
    def wrapper(*args, **kwargs):
        with Session() as db:
            kwargs['db'] = db
            return func(*args, **kwargs)
    return wrapper


class BookRepository:
    def find(self, book_id: int):
        with Session() as db:
            return db.query(models.Book).filter(models.Book.id == book_id).first()

    def list(self, limit: int = 100):
        with Session() as db:
            books = db.query(models.Book).limit(limit).all()
            [book.author for book in books]
            return books

    def retrieve_by_title(self, book_title: str):
        with Session() as db:
            return db.query(models.Book).filter(models.Book.title == book_title).all()

    def create(self, book: schemas.BookCreate):
        with Session() as db:
            new_book = models.Book(
                title=book.title,
                author_id=book.author_id,
                release_date=book.release_date,
                number_of_pages=book.number_of_pages,
                image_url=book.image_url
            )
            db.add(new_book)
            db.commit()
            db.refresh(new_book)
            return new_book

    def delete(self, book_id):
        with Session() as db:
            book = db.query(models.Book).filter(
                models.Book.id == book_id).first()
            if book is None:
                return
            db.delete(book)
            db.commit()
            return book


class AuthorRepository:
    def find(self, author_id: int) -> models.Author:
        with Session() as db:
            author = db.query(models.Author).where(
                models.Author.id == author_id).first()
            if author is None:
                raise HTTPException(400, 'this author could not be found')
            author.books
            return author

    def find_by_name(self, author_name: str):
        with Session() as db:
            return db.query(models.Author).where(models.Author.first_name.ilike(author_name) or models.Author.last_name.ilike(author_name)).all()

    # @db_session
    def list(self, limit: int, db=Session()):
        with Session() as db:
            authors = db.query(models.Author).limit(limit).all()
            [author.books for author in authors]
            return authors

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

    def delete(self, author_id):
        with Session() as db:
            author = db.query(models.Author).where(
                models.Author.id == author_id).first()
            if author is None:
                return
            db.delete(author)
            db.commit()
            return author
