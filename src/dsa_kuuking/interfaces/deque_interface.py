from abc import ABC, abstractmethod

from dsa_kuuking.types.ResultType import ResultType
from dsa_kuuking.interfaces.queue_interface import QueueInterface


class DequeInterface[T](QueueInterface, ABC):
    @abstractmethod
    def enqueue_front(self, element: T) -> None: ...

    @abstractmethod
    def enqueue_rear(self, element: T) -> None: ...

    @abstractmethod
    def dequeue_front(self) -> ResultType[T, str]: ...

    @abstractmethod
    def dequeue_rear(self) -> ResultType[T, str]: ...

    @abstractmethod
    def get_peek_front(self) -> ResultType[T, str]: ...

    @abstractmethod
    def get_peek_rear(self) -> ResultType[T, str]: ...

    @abstractmethod
    def peek_front(self) -> None: ...

    @abstractmethod
    def peek_rear(self) -> None: ...
