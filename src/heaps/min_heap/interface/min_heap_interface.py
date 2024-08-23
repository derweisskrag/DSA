from abc import ABC, abstractmethod
from typing import Iterable, List


class MinHeapInterface[T](ABC):
    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def peek(self) -> None: ...

    @abstractmethod
    def get_peek(self) -> T: ...

    @abstractmethod
    def is_empty(self) -> bool: ...

    @abstractmethod
    def is_leaf(self, index: int) -> bool: ...

    @abstractmethod
    def has_left_child(self, index: int) -> bool: ...

    @abstractmethod
    def has_right_child(self, index: int) -> bool: ...

    @abstractmethod
    def has_parent(self, index: int) -> bool: ...

    @abstractmethod
    def swap(self, i: int, j: int) -> None: ...

    @abstractmethod
    def display(self) -> None: ...

    @abstractmethod
    def traverse(self) -> Iterable[T]: ...

    @abstractmethod
    def traverse_backwards(self) -> Iterable[T]: ...

    @abstractmethod
    def pop(self) -> T: ...

    @abstractmethod
    def insert(self, element: T) -> None: ...

    @abstractmethod
    def insert_many(self, elements: Iterable[T]) -> None: ...

    @abstractmethod
    def heapify_up(self, index: int) -> None: ...

    @abstractmethod
    def heapify_down(self, index: int) -> None: ...

    @abstractmethod
    def heapify(self, list_of_elements: List[T]) -> None: ...

    @abstractmethod
    def get_smallest_child_index(self, index: int) -> int: ...





