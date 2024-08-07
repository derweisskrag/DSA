from typing import override, Iterable

from src.linked_lists.Exceptions.LinkedListEmptyException import LinkedListEmptyException
from src.linked_lists.linked_list.implementation.linked_list import LinkedList
from src.linked_lists.types.ResultType import ResultType
from src.queues.queue.interface.queue_interface import QueueInterface


class Queue[T](QueueInterface):
    def __init__(self):
        self._queue = LinkedList[T]()

    @override
    def enqueue(self, element: T) -> None:
        result = self._queue.add_to_front(element)

        if result.is_ok():
            print("Success! The element has been enqueued!")
        else:
            print(f"An error occurred: {result.unwrap_err()}")

    @override
    def dequeue(self) -> ResultType[T, str]:
        result = self.get_peek()
        if not result.is_ok():
            raise LinkedListEmptyException(message=result.unwrap_err())

        return result

    @override
    def peek(self) -> None:
        result = self.get_peek()

        if result.is_ok():
            print("The (front) peek is ", result.unwrap())
        else:
            print(f"An error occurred: {result.unwrap_err()}")

    @override
    def is_empty(self) -> bool:
        return self._queue.is_empty()

    @override
    def traverse(self) -> Iterable[T]:
        for element in self._queue.traverse():
            yield element

    @override
    def display(self) -> None:
        self._queue.display()

    @override
    def manage_size(self, action: str) -> ResultType[str, str]:
        raise NotImplemented("This method is not intended")

    @override
    def get_peek(self) -> ResultType[T, str]:
        return ResultType(value=self._queue.get_head().unwrap())
