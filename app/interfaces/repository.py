from abc import ABC, abstractmethod
from typing import Any


class Repository(ABC):
    @abstractmethod
    def find(self, id: int) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def list(self) -> list[Any]:
        raise NotImplementedError()

    @abstractmethod
    def create(self, model: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, author_id: int) -> bool:
        raise NotImplementedError()
