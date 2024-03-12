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
        author = self.session.scalars(
            select(T.__class__).where(T.__class__.id == id)
        ).first()
        if author is None:
            return None
        return author

    def list(self) -> list[T]:
        author_models = self.session.scalars(select(T.__class__)).all()
        return [author.to_entity() for author in author_models]

    @abstractmethod
    def create(self, model: Any) -> Any:
        raise NotImplementedError()

    def delete(self, book_id: int) -> bool:
        book = self.session.scalars(
            select(T.__class__).where(T.__class__.id == book_id)
        ).first()
        if book is None:
            return False
        self.session.delete(book)
        self.session.commit()
        return True
