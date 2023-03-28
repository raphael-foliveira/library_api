from datetime import date
from typing import Optional
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    release_date: date
    number_of_pages: int
    author_id: int
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    ...


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
