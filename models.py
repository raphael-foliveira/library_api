from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, DeclarativeBase
from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    release_date = Column(Date)
    number_of_pages = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))
    image_url = Column(String)

    author = relationship("Author", back_populates="books")
