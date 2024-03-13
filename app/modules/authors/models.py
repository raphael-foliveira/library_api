from typing import Any
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, mapped_column
from app.database.config import Base
from app.modules.authors.entities import Author


class AuthorModel(Base):
    __tablename__ = "authors"

    id = mapped_column(Integer, primary_key=True, index=True)
    first_name = mapped_column(String)
    last_name = mapped_column(String)

    books = relationship("BookModel", back_populates="author")

    def __eq__(self, other: Any):
        return self.id == other.id

    def to_entity(self) -> Author:
        return Author(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
        )
