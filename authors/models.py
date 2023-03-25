from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)

    books = relationship("Book", back_populates="author", lazy="joined")
