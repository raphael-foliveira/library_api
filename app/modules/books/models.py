from typing import Any
from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column
from app.database.config import Base


class Book(Base):
    __tablename__ = "books"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String)
    release_date = mapped_column(Date)
    number_of_pages = mapped_column(Integer)
    author_id = mapped_column(Integer, ForeignKey("authors.id"))
    image_url = mapped_column(String, nullable=True)

    author = relationship(
        "Author", back_populates="books", lazy="joined", cascade="all, delete"
    )

    def __eq__(self, other: Any):
        return self.id == other.id
