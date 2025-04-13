from abc import ABC, abstractmethod

from dsa_kuuking.interfaces.min_heap_interface import MinHeapInterface


class MaxHeapInterface[T](MinHeapInterface, ABC):
    @abstractmethod
    def get_largest_index(self, index: int) -> int: ...
