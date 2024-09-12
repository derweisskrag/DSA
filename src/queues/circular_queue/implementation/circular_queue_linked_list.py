from typing import override

from src.linked_lists.circular_linked_list.implementation.circular_linked_list import CircularLinkedList
from src.types.ResultType import ResultType
from src.interfaces.circular_queue_interface import CircularQueueInterface
from src.queues.queue.implementation.queue_linked_list import Queue


class CircularQueue[T](CircularQueueInterface, Queue):
    def __init__(self):
        super().__init__()
        self._circular_queue = CircularLinkedList[int]()

    @override
    def enqueue(self, element: T) -> None:
        result = self._circular_queue.add_to_front(element)

        if result.is_ok():
            print("Success! The element has been added: ", result.unwrap().data)
        else:
            raise Exception(result.unwrap_err())

    @override
    def dequeue(self) -> ResultType[T, str]:
        result = self._circular_queue.remove_head()

        if result is not None:
            print("Success! The element has been dequeued: ", result.data)

        return ResultType(error="Failure! Cannot remove the element!")

    @override
    def get_peek(self) -> ResultType[T, str]:
        result = self._circular_queue.get_head()

        if result.is_ok():
            return ResultType(value=result.unwrap())

        return ResultType(error=result.unwrap_err())

    @override
    def peek(self) -> None:
        result = self.get_peek()
        if result.is_ok():
            print("The peek is ", result.unwrap().data)
        else:
            print("An error: ", result.unwrap_err())

    @override
    def is_empty(self) -> bool:
        return self._circular_queue.is_empty()

    @override
    def display(self) -> None:
        self._circular_queue.display()

    @override
    def manage_size(self, action: str) -> ResultType[str, str]:
        raise NotImplemented("This method is not intended! Please, use you queue implemented using a list!")

    @override
    def is_full(self) -> bool:
        raise NotImplemented("This method is not intended! Please, use you queue implemented using a list!")
