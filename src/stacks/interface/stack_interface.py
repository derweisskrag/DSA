from abc import ABC, abstractmethod
from typing import Iterable


class StackInterface[T](ABC):
    @abstractmethod
    def append(self, element: T) -> None: ...

    @abstractmethod
    def pop(self) -> T: ...

    @abstractmethod
    def peek(self) -> None: ...

    @abstractmethod
    def is_empty(self) -> bool: ...

    @abstractmethod
    def display(self) -> None: ...

    @abstractmethod
    def traverse(self) -> Iterable[T]: ...
