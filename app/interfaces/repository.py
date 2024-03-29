from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session


@dataclass
class Entity:
    id: int


T = TypeVar("T", bound=Entity)


class Repository(ABC, Generic[T]):

    def __init__(self, session: Session):
        self.session = session

    def find(self, id: int) -> Optional[T]:
        statement = select(T.__class__).where(T.__class__.id == id)
        author = self.session.scalars(statement).first()
        if author is None:
            return None
        return author

    def list(self) -> list[T]:
        statement = select(T.__class__)
        author_models = self.session.scalars(statement).all()
        return [author.to_entity() for author in author_models]

    @abstractmethod
    def create(self, model: Any) -> T:
        raise NotImplementedError()

    def delete(self, book_id: int) -> bool:
        statement = select(T.__class__).where(T.__class__.id == book_id)
        book = self.session.scalars(statement).first()
        if book is None:
            return False
        self.session.delete(book)
        self.session.commit()
        return True
