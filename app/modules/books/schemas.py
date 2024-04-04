from datetime import date
from typing import Optional, TypedDict
from ..authors.schemas import Author
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    release_date: date
    number_of_pages: int
    author_id: int
    image_url: Optional[str] = None


class CreateBook(BookBase):
    pass


class Book(BookBase):
    id: int


class BookAuthor(BaseModel):
    id: int
    first_name: str
    last_name: str


class BookDetails(BaseModel):
    id: int
    title: str
    release_date: date
    number_of_pages: int
    author: BookAuthor


def book_details(book: Book, author: Author):
    book_author = BookAuthor(
        id=author.id, first_name=author.first_name, last_name=author.last_name
    )
    return BookDetails(
        id=book.id,
        title=book.title,
        release_date=book.release_date,
        number_of_pages=book.number_of_pages,
        author=book_author,
    )
