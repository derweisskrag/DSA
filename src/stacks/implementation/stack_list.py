from typing import List, override, Set, Iterable

from src.interfaces.stack_interface import StackInterface


class Stack[T](StackInterface):
    def __init__(self):
        self.size: int = 0
        self._hash_set: Set[T] = set()
        self._stack: List[T] = []

    @override
    def append(self, element: T) -> None:
        self._stack.append(element)
        self._hash_set.add(element)
        self.size += 1

    @override
    def pop(self) -> T:
        self._hash_set.remove(self._stack[-1])
        self.size -= 1
        return self._stack.pop()

    @override
    def peek(self) -> None:
        print(self._stack[-1])

    @override
    def display(self) -> None:
        for element in self.traverse():
            print(element, end="->" if element is not None else "")

    @override
    def traverse(self) -> Iterable[T]:
        for element in self._stack:
            yield element

    @override
    def is_empty(self) -> bool:
        return self.size == 0

    def __contains__(self, element: T) -> bool:
        return element in self._hash_set
