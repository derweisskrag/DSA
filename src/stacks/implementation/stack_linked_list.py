from typing import override, Iterable

from src.types.errors.LinkedListEmptyException import LinkedListEmptyException
from src.linked_lists.linked_list.implementation.linked_list import LinkedList
from src.interfaces.stack_interface import StackInterface


class Stack[T](StackInterface):
    def __init__(self):
        self._stack = LinkedList[T]()

    @override
    def append(self, element: T) -> None:
        self._stack.add_to_front(element)

    @override
    def pop(self) -> T:
        result = self._stack.peek_last()
        if result.is_ok():
            return result.unwrap().data  # Assuming the user wants the data of type T
        else:
            # Handle exceptions
            error_message = result.unwrap_err()
            raise LinkedListEmptyException(message=error_message)

    @override
    def display(self) -> None:
        self._stack.display()

    @override
    def peek(self) -> None:
        print(self._stack[-1])

    @override
    def traverse(self) -> Iterable[T]:
        for element in self._stack.traverse():
            yield element

    @override
    def is_empty(self) -> bool:
        return self._stack.is_empty()
