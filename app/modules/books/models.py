from typing import Any
from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column
from app.database.config import Base
from app.modules.books.schemas import Book


class BookModel(Base):
    __tablename__ = "books"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String)
    release_date = mapped_column(Date)
    number_of_pages = mapped_column(Integer)
    author_id = mapped_column(Integer, ForeignKey("authors.id"))
    image_url = mapped_column(String, nullable=True)

    author = relationship(
        "AuthorModel", back_populates="books", lazy="joined", cascade="all, delete"
    )

    def __eq__(self, other: Any):
        return self.id == other.id

    def to_entity(self) -> Book:
        return Book(
            id=self.id,
            title=self.title,
            release_date=self.release_date,
            number_of_pages=self.number_of_pages,
            author_id=self.author_id,
            image_url=self.image_url,
        )
