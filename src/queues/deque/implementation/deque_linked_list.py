from typing import override, Iterable

from src.types.errors.LinkedListEmptyException import LinkedListEmptyException
from src.linked_lists.doubly_linked_list.implementation.doubly_linked_list import DoublyLinkedList
from src.types.ResultType import ResultType
from src.interfaces.deque_interface import DequeInterface
from src.queues.queue.implementation.queue_linked_list import Queue


class Deque[T](DequeInterface, Queue):
    def __init__(self):
        super().__init__()
        self._deque = DoublyLinkedList[T]()

    @override
    def enqueue_front(self, element: T) -> None:
        result = self._deque.add_to_front(element)

        if result.is_ok():
            print("Success! The element has been enqueued to front!")
        else:
            print(f"An error occurred: {result.unwrap_err()}")

    @override
    def enqueue_rear(self, element: T) -> None:
        result = self._deque.add_to_end(element)

        if result.is_ok():
            print("Success! The element has been enqueued to rear!")
        else:
            print(f"An error occurred: {result.unwrap_err()}")

    @override
    def dequeue_front(self) -> ResultType[T, str]:
        result = ResultType(value=self._deque.remove_head())

        if result.is_ok():
            print("Success! The element has been dequeued from front!")
            return result
        else:
            # Handle exceptions
            raise LinkedListEmptyException(message=result.unwrap_err())

    @override
    def dequeue_rear(self) -> ResultType[T, str]:
        result = ResultType(value=self._deque.remove_tail())

        if not result.is_ok():
            raise LinkedListEmptyException(message=result.unwrap_err())

        return result

    @override
    def get_peek_front(self) -> ResultType[T, str]:
        return super().get_peek()

    @override
    def get_peek_rear(self) -> ResultType[T, str]:
        result = self._deque.get_tail()

        if result.is_ok():
            return ResultType(value=self._deque.get_tail().unwrap())
        else:
            return ResultType(error=result.unwrap_err())

    @override
    def peek_front(self) -> None:
        super().peek()

    @override
    def peek_rear(self) -> None:
        result = self.get_peek_rear()

        if result.is_ok():
            print("The rear peek is ", result.unwrap())
        else:
            # handle exception
            print(f"An error occurred: {result.unwrap_err()}")

    @override
    def display(self) -> None:
        self._deque.display()

    @override
    def traverse(self) -> Iterable[T]:
        for element in self._deque.traverse():
            yield element

    @override
    def is_empty(self) -> bool:
        return self._deque.is_empty()
