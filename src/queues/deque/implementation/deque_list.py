from typing import Set, List, override

from src.types.ResultType import ResultType
from src.types.errors.empty_queue_exception import EmptyQueueException
from src.types.errors.size_management_exception import SizeManagementException
from src.interfaces.deque_interface import DequeInterface
from src.queues.queue.implementation.queue_list import Queue


class Deque[T](DequeInterface, Queue):
    def __init__(self):
        super().__init__()
        self.count = 0
        self._hash_set: Set[T] = set()
        self._deque: List[T] = []

    @override
    def enqueue_front(self, element: T) -> None:
        super().enqueue(element)

    @override
    def enqueue_rear(self, element: T) -> None:
        # update the size
        result = super().manage_size(action="enqueue", value=element)

        if result.is_ok():
            print(result.unwrap())
            self._deque.append(element)
        else:
            raise Exception(result.unwrap_err())

    @override
    def dequeue_front(self) -> ResultType[T, str]:
        return super().dequeue()

    @override
    def dequeue_rear(self) -> ResultType[T, str]:
        # get the peek
        peek_rear_result = self.get_peek_rear()

        if peek_rear_result.is_ok():
            # update the size
            result = super().manage_size(action="dequeue", value=peek_rear)

            if result.is_ok():
                print(result.unwrap())
                return ResultType(value=self._deque.pop())
            else:
                raise SizeManagementException(result.unwrap_err())
        else:
            raise EmptyQueueException(peek_rear_result.unwrap_err())

    @override
    def get_peek_front(self) -> ResultType[T, str]:
        return ResultType(value=super().peek())

    @override
    def get_peek_rear(self) -> ResultType[T, str]:
        if self.is_empty():
            return ResultType(error="Cannot retrieve the rear peek from the empty dequeue!")

        # get peek
        peek_rear = self._deque[-1]

        if peek_rear is None:
            return ResultType(error=f"Rear peek is not defined: {peek_rear}")

        # return it
        return ResultType(value=peek_rear)

    @override
    def peek_rear(self) -> None:
        # fetch rear_peek
        result = self.get_peek_rear()

        if result.is_ok():
            print("Rear peek is ", result.unwrap())
        else:
            raise Exception(result.unwrap_err())

    @override
    def peek_front(self) -> None:
        super().peek()

    @override
    def display(self) -> None:
        if self.is_empty():
            print("The dequeue is empty: Deque()")

        print("<-->".join(map(str, self._deque)))
