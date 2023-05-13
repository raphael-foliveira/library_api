from abc import ABC, abstractmethod
from typing import Any


class Repostory(ABC):
    @abstractmethod
    def find(self, id: int) -> Any:
        pass

    @abstractmethod
    def list(self) -> list[Any]:
        pass

    @abstractmethod
    def create(self, model: Any) -> Any:
        pass

    @abstractmethod
    def delete(self, author_id: int) -> bool:
        pass
