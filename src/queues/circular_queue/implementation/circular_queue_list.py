from typing import List, Set, override

from src.linked_lists.types.ResultType import ResultType
from src.queues.Exceptions.size_management_exception import SizeManagementException
from src.queues.circular_queue.interface.circular_queue_interface import CircularQueueInterface
from src.queues.queue.implementation.queue_list import Queue


class CircularQueue[T](CircularQueueInterface, Queue):
    def __init__(self, maxsize: int = 10):
        super().__init__()
        self._circular_queue: List[T] = [0] * maxsize
        self._hash_set: Set[T] = set()
        self.size: int = maxsize

        # pointer to the head
        self._front = 0

        # numbers of enqueued elements
        self.count = 0

    @override
    def enqueue(self, element: T) -> None:
        if self.is_full():
            # handle when circular queue is full
            raise Exception("Queue is full")

        # enqueue the element
        self._circular_queue[(self._front + self.count) % self.size] = element

        # manage the size
        result = self.manage_size(action="enqueue", value=element)

        if result.is_ok():
            print(result.unwrap())
        else:
            print("An error happened: ", result.unwrap_err())

    @override
    def dequeue(self) -> ResultType[T, str]:
        # defined the element to deque
        dequeued_element = self._circular_queue[self._front]

        # remove it
        self._circular_queue[self._front] = None

        # update the circular queue's front pointer
        self._front = (self._front + 1) % self.size

        # update the size and hash_set
        manage_size_result = self.manage_size(action="dequeue", value=dequeued_element)

        if manage_size_result.is_ok():
            print(manage_size_result.unwrap())
        else:
            raise SizeManagementException(manage_size_result.unwrap_err())

        # return the dequeued element
        return ResultType(value=dequeued_element)

    @override
    def is_full(self) -> bool:
        return self.size == self.count

    @override
    def peek(self) -> None:
        result = self.get_peek()

        if result.is_ok():
            print("The peek is ", result.unwrap())
        else:
            print(result.unwrap_err())

    @override
    def get_peek(self) -> ResultType[T, str]:
        if self.is_empty():
            return ResultType(error="Cannot retrieve the peek from empty queue!")

        return ResultType(value=self._circular_queue[self._front])

