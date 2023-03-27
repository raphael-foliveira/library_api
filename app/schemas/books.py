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
