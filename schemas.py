from datetime import date
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    release_date: date
    number_of_pages: int
    author_id: int
    image_url: str | None

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    first_name: str
    last_name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
