from typing import override, Union, Optional, Iterable

from dsa_kuuking.interfaces.circular_linked_list_interface import CircularLinkedListInterface
from dsa_kuuking.linked_lists.linked_list.implementation.linked_list import LinkedList
from dsa_kuuking.types.nodes.NodeType import NodeType
from dsa_kuuking.types.ResultType import ResultType


class CircularLinkedList[T](CircularLinkedListInterface, LinkedList):
    def __init__(self):
        super().__init__()
        self._tail = None

    @override
    def balance_list(self):
        # ensure the circularity
        self._tail.next = self._head
        self._head.prev = self._tail

    @override
    def insert_node(self, data: Union[T, NodeType[T]], position: int) -> Optional[ResultType[NodeType[T], str]]:
        result = super().insert_node(data, position)
        self.balance_list()
        return result

    @override
    def remove_by_data(self, data: T) -> Optional[NodeType[T]]:
        result = super().remove_by_data(data)
        self.balance_list()
        return result

    @override
    def remove_head(self) -> Optional[NodeType[T]]:
        # TODO: Consider refactor (maybe self.remove_by_data(self._head.data))
        result = super().remove_head()
        self.balance_list()
        return result

    @override
    def display(self) -> None:
        for node in self.traverse():
            print(node, end="<-->" if node.next else "\n")

        # print the head for circular view
        print(self._head)

    @override
    def traverse(self) -> Iterable[NodeType[T]]:
        current = self._head
        yield current
        while current.next != self._head:
            current = current.next
            yield current

    @override
    def reverse(self) -> Optional['LinkedList[T]']:
        current = self._head
        prev = None
        self._tail = self._head
        while True:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
            if current == self._head:
                break

        # restore linked list
        self._head.next = prev
        self._head = prev

        # make sure circular behavior
        self.balance_list()

        # return the reversed linked list
        return self

    @override
    def traverse_backwards(self) -> Iterable[NodeType[T]]:
        for node in self.reverse().traverse():
            yield node

    @override
    def display_backwards(self) -> None:
        for node in self.traverse_backwards():
            print(node, end="<-->" if node.next else "\n")

        print(self._head)
