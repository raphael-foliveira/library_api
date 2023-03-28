from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    release_date = Column(Date)
    number_of_pages = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))
    image_url = Column(String, nullable=True)

    author = relationship("Author", back_populates="books", lazy="joined")

    def __eq__(self, other):
        return self.id == other.id
