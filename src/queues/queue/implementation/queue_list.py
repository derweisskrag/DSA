from typing import Set, override, List, Iterable

from src.types.ResultType import ResultType
from src.types.errors.empty_queue_exception import EmptyQueueException
from src.types.errors.size_management_exception import SizeManagementException
from src.interfaces.queue_interface import QueueInterface


class Queue[T](QueueInterface):
    def __init__(self):
        self.count = 0
        self._hash_set: Set[T] = set()
        self._queue: List[T] = []

    @override
    def enqueue(self, element: T) -> None:
        # update the size
        result = self.manage_size(action="enqueue", value=element)

        if result.is_ok():
            print(result.unwrap())
            self._queue.insert(0, element)
        else:
            raise Exception(result.unwrap_err())

    @override
    def dequeue(self) -> ResultType[T, str]:
        # peek
        peek_result = self.get_peek()

        if peek_result.is_ok():
            # update the list
            result = self.manage_size(action="dequeue", value=peek_result.unwrap())

            if result.is_ok():
                print(result.unwrap())
                return ResultType(value=self._queue.pop(0))
            else:
                # handle the error
                raise SizeManagementException(result.unwrap_err())
        else:
            raise EmptyQueueException(peek_result.unwrap_err())

    @override
    def get_peek(self) -> ResultType[T, str]:
        if self.is_empty():
            return ResultType(error="Cannot retrieve the peek from empty queue!")

        # get the peek value
        peek_value = self._queue[0]

        if peek_value is None:
            return ResultType(error="Peek value is not defined")

        # return
        return ResultType(value=peek_value)

    @override
    def peek(self) -> None:
        # try to get peek
        result = self.get_peek()

        if result.is_ok():
            print("Peek is ", result.unwrap())
        else:
            raise Exception(result.unwrap_err())

    @override
    def is_empty(self) -> bool:
        return self.count == 0

    @override
    def traverse(self) -> Iterable[T]:
        for element in self._queue:
            yield element

    @override
    def display(self) -> None:
        if self.is_empty():
            print("Queue is empty: Queue()")

        print(self._queue)

    @override
    def manage_size(self, action: str = "", value: T = None) -> ResultType[str, str]:
        match action:
            case "enqueue":
                self.count += 1
                self._hash_set.add(value)
                return ResultType(value="Success! The value has been enqueued!")
            case "dequeue":
                self.count -= 1
                self._hash_set.remove(value)
                return ResultType(value="Success! The value has been dequeued!")
            case _:
                return ResultType(error="Wrong action!")

    def __contains__(self, element: T) -> bool:
        return element in self._hash_set

    def __str__(self) -> str:
        return "->".join(map(str, self._queue))

    def __len__(self) -> int:
        return self.count
