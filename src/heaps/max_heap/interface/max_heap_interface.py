from abc import ABC, abstractmethod

from src.heaps.min_heap.interface.min_heap_interface import MinHeapInterface


class MaxHeapInterface[T](MinHeapInterface, ABC):
    @abstractmethod
    def get_largest_index(self, index: int) -> int: ...
