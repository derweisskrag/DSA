from typing import override, List

from dsa_kuuking.interfaces.max_heap_interface import MaxHeapInterface
from dsa_kuuking.heaps.min_heap.implementation.min_heap import MinHeap


class MaxHeap[T](MinHeap, MaxHeapInterface):
    def __init__(self):
        super().__init__()
        self._max_heap: List[T] = []

    @override
    def heapify_down(self, index: int) -> None:
        while self.has_left_child(index):
            ...

    @override
    def heapify_up(self, index: int) -> None: ...

    @override
    def get_largest_index(self, index: int) -> int:
        if self.has_right_child(index):
            return max(self.left_child(index), self.right_child(index), key=lambda i: self._max_heap[i])

        return self.left_child(index)
