from abc import ABC, abstractmethod


class CircularQueueInterface[T](ABC):
    @abstractmethod
    def enqueue(self, element: T) -> None: ...

    @abstractmethod
    def is_full(self) -> bool: ...