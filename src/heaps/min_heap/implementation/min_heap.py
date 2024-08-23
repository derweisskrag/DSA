from math import floor, log2
from typing import List, override, Iterable

from src.heaps.min_heap.interface.min_heap_interface import MinHeapInterface


class MinHeap[T](MinHeapInterface):
    def __init__(self):
        self._min_heap: List[T] = []

    @override
    def size(self) -> int:
        return len(self._min_heap)

    @override
    def is_empty(self) -> bool:
        return len(self._min_heap) == 0

    @override
    def is_leaf(self, index: int) -> bool:
        return not (self.has_left_child(index) or self.has_right_child(index))

    @override
    def has_left_child(self, index: int) -> bool:
        return self.left_child(index) < len(self._min_heap)

    @override
    def has_right_child(self, index: int) -> bool:
        return self.right_child(index) < len(self._min_heap)

    @override
    def has_parent(self, index: int) -> int:
        return self.parent(index) >= 0

    @staticmethod
    def left_child(index: int) -> int:
        return 2 * index + 1

    @staticmethod
    def right_child(index: int) -> int:
        return 2 * index + 2

    @staticmethod
    def parent(index: int) -> int:
        return (index - 1) // 2

    @staticmethod
    def _level(index: int) -> float:
        return floor(log2(index + 1))

    @override
    def swap(self, i: int, j: int) -> None:
        self._min_heap[i], self._min_heap[j] = self._min_heap[j], self._min_heap[i]

    @override
    def display(self) -> None:
        levels = self._level(self.size() - 1) + 1
        symbols = max(len(str(x)) for x in self._min_heap)
        row = ""

        for index, element in enumerate(self._min_heap):
            current_level = self._level(index)
            distance = 2 ** ((levels - current_level) * symbols)

            # print the node
            elem_str = f"{element if element else "": ^{symbols}}"
            print(f"{elem_str: ^{distance}}", sep="", end="")

            lines = "/" if self.has_left_child(index) else " "
            lines += " " * symbols
            lines += "\\" if self.has_right_child(index) else " "
            row += f"{lines:^{distance}}"

            # At the end of level add Edges row
            if index + 1 == (2 ** (current_level + 1) - 1):
                print()
                lines = "/ \\"
                print(row, sep="")
                row = ""

        print()

    @override
    def traverse(self) -> Iterable[T]:
        for index in range(len(self._min_heap)):
            yield index

    @override
    def traverse_backwards(self) -> Iterable[T]:
        for index in range(len(self._min_heap) - 1, -1, -1):
            yield index

    @override
    def peek(self) -> None:
        peek = self.get_peek()
        # handle errors
        print(f"Peek: {peek}")

    @override
    def get_peek(self) -> T:
        return self._min_heap[0]

    @override
    def pop(self) -> T:
        # swap root with the last index
        self.swap(0, len(self._min_heap) - 1)

        # pop the last element
        result = self._min_heap.pop()

        # restore the min heap property
        self.heapify_down(0)

        # return extracted element
        return result

    @override
    def insert(self, element: T) -> None:
        self._min_heap.append(element)
        self.heapify_up(len(self._min_heap) - 1)

    @override
    def insert_many(self, elements: Iterable[T]) -> None:
        for value in elements:
            self.insert(value)

    @override
    def heapify_up(self, index: int) -> None:
        # you cannot go up if no parent
        # example:
        #           1
        #         /   \
        #        2     3
        #       / \
        #      4   5
        #
        # How to go from 3 to 1? Using the parent index!

        while self.has_parent(index) and self._min_heap[self.parent(index)] > self._min_heap[index]:
            # get parent index
            parent_index = self.parent(index)

            # swap (condition is in the while loop)
            self.swap(index, parent_index)

            # to next iteration
            index = parent_index

    @override
    def heapify_down(self, index: int) -> None:
        # after we extracted the least element
        # our root is not balanced: not the smallest
        # also we should traverse the heap in the way find the smallest

        # define the smallest
        smallest_element_index = None

        # traverse the heap until we end up
        # in leaf
        while not self.is_leaf(index):
            if self.has_left_child(index):
                # we have the left child
                smallest_element_index = self.left_child(index)

            if self.has_right_child(index):
                # get the right child
                right_child_index = self.right_child(index)

                # now we have to check if it is the smallest
                if self._min_heap[smallest_element_index] > self._min_heap[right_child_index]:
                    smallest_element_index = right_child_index

            # swap if parent is greater than the smallest child
            if self._min_heap[smallest_element_index] > self._min_heap[index]:
                # swap
                self.swap(index, smallest_element_index)

            # next iteration
            index = smallest_element_index

    def _heapify_down(self, index):
        while self.has_left_child(index):
            # retrieve the smallest index
            smallest_index = self.get_smallest_child_index(index)

            # exit loop when is_leaf
            if self.is_leaf(index):
                break

            # swap
            self.swap(index, smallest_index)

            # to the next iteration
            index = smallest_index

    @override
    def heapify(self, list_of_elements: List[T]) -> 'MinHeap[T]':
        """Heapify the list to make a MinHeap from an input list.

        Args:
            list_of_elements (list[int]): the list of data to heapify.

        Examples:
            Example 1.
            MinHeap([]) - empty heap
            list_of_elements = [12, 15, 25, 16, 3] - input array
            returns: MinHeap([3, 12, 25, 16, 15]) - result

            Example 2.
            MinHeap([3, 12, 25, 16, 15]) - not empty heap
            arr = [
                1, 2, 3, 4, 5, 6, 7, 8, 9,
                10, 11, 12, 13, 14, 15]
            returns: MinHeap([
                1, 1, 3, 2, 3, 6, 7, 4,
                9, 5, 11, 12, 13, 14, 15,
                8, 12, 15, 25, 16, 10])

        Returns:
            It returns the MinHeap (self).
        """

        self.insert_many(list_of_elements)

        return self

    def _heapify(self, list_of_elements: List[T]) -> 'MinHeap[T]':
        """Heapify the list to make a MinHeap from an input list.

        Args:
            list_of_elements (list[int]): the list of data to heapify.

        Examples:
            Example 1.
            MinHeap([]) - empty heap
            list_of_elements = [12, 15, 25, 16, 3] - input array
            returns: MinHeap([3, 12, 25, 16, 15]) - result

            Example 2.
            MinHeap([3, 12, 25, 16, 15]) - not empty heap
            arr = [
                1, 2, 3, 4, 5, 6, 7, 8, 9,
                10, 11, 12, 13, 14, 15]
            returns: MinHeap([
                1, 1, 3, 2, 3, 6, 7, 4,
                9, 5, 11, 12, 13, 14, 15,
                8, 12, 15, 25, 16, 10])

        Returns:
            It returns the MinHeap (self).
        """

        # modify the heap
        self._min_heap = self._min_heap + list_of_elements

        # traverse backward and apply heapify_app
        for index in self.traverse_backwards():
            self.heapify_up(index)

        return self

    @override
    def get_smallest_child_index(self, index: int) -> int:
        if self.has_right_child(index):
            return min(self.left_child(index), self.right_child(index), key=lambda i: self._min_heap[i])

        return self.left_child(index)
