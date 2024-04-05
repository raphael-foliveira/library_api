from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar
from sqlalchemy import select
from sqlalchemy.orm.session import sessionmaker


@dataclass
class Entity:
    id: int


T = TypeVar("T", bound=Entity)


class Repository(Generic[T]):

    def __init__(self, session: sessionmaker, entity_class: T.__class__):
        self.session = session
        self.entity_class = entity_class

    def find_one(self, id: int) -> Optional[T]:
        with self.session() as db:
            statement = select(self.entity_class).where(self.entity_class.id == id)
            author = db.scalars(statement).first()
            if author is None:
                return None
            return author

    def list(self) -> list[T]:
        with self.session() as db:
            statement = select(self.entity_class)
            author_models = db.scalars(statement).all()
            return [author.to_entity() for author in author_models]

    @abstractmethod
    def create(self, model: Any) -> T:
        raise NotImplementedError()

    def delete(self, book_id: int) -> bool:
        with self.session() as db:
            statement = select(self.entity_class).where(self.entity_class.id == book_id)
            book = db.scalars(statement).first()
            if book is None:
                return False
            db.delete(book)
            db.commit()
            return True
