from abc import ABC, abstractmethod
from typing import Iterable

from src.types.ResultType import ResultType


class QueueInterface[T](ABC):
    @abstractmethod
    def enqueue(self, element: T) -> None: ...

    @abstractmethod
    def dequeue(self) -> ResultType[T, str]: ...

    @abstractmethod
    def get_peek(self) -> ResultType[T, str]: ...

    @abstractmethod
    def peek(self) -> None: ...

    @abstractmethod
    def is_empty(self) -> bool: ...

    @abstractmethod
    def traverse(self) -> Iterable[T]: ...

    @abstractmethod
    def display(self) -> None: ...

    @abstractmethod
    def manage_size(self, action: str) -> ResultType[str, str]: ...
