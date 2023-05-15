from typing import Any
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)

    books = relationship("Book", back_populates="author", lazy="joined")

    def __eq__(self, other: Any):
        return self.id == other.id
