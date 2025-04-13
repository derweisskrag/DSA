from typing import Optional, Iterable, override, Union

from dsa_kuuking.types.errors.LinkedListEmptyException import LinkedListEmptyException
from dsa_kuuking.interfaces.doubly_linked_list_interface import DoublyLinkedListInterface
from dsa_kuuking.linked_lists.linked_list.implementation.linked_list import LinkedList
from dsa_kuuking.types.nodes.DoublyLinkedListNode import DoublyLinkedListNode as Node
from dsa_kuuking.types.nodes.NodeType import NodeType
from dsa_kuuking.types.ResultType import ResultType


class DoublyLinkedList[T](LinkedList, DoublyLinkedListInterface):
    """
    A generic doubly linked list implementation.

    This class implements a doubly linked list using nodes of type `Node[T]`.
    Each node contains references to both the previous and next nodes in the list,
    allowing for efficient bidirectional traversal. It supports operations such as
    adding nodes to the front or end of the list, removing nodes, and traversing
    the list in both directions.

    Attributes:
        _head (Optional[Node[T]]): The head node of the doubly linked list. Initialized to None.
        _tail (Optional[Node[T]]): The tail node of the doubly linked list. Initialized to None.

    Methods:
        add_to_front(data: T) -> None: Adds a new node with the given data to the front of the list.
        add_to_end(data: T) -> None: Adds a new node with the given data to the end of the list.
        remove_head() -> Optional[Node[T]]: Removes and returns the node from the front of the list.
        remove_tail() -> Optional[Node[T]]: Removes and returns the node from the end of the list.
        traverse_forward() -> Iterator[Node[T]]: Traverses the list from head to tail, yielding nodes.
        traverse_backward() -> Iterator[Node[T]]: Traverses the list from tail to head, yielding nodes.

    Example:
        >>> dll = DoublyLinkedList[int]()
        >>> dll.add_to_front(10)
        >>> dll.add_to_end(20)
        >>> dll.add_to_front(5)
        >>> list(dll.traverse_forward())
        [Node(data=5), Node(data=10), Node(data=20)]
        >>> list(dll.traverse_backwards())
        [Node(data=20), Node(data=10), Node(data=5)]
        >>> dll.remove_tail()
        Node(data=20)
        >>> dll.remove_head()
        Node(data=5)
    """

    def __init__(self) -> None:
        super().__init__()
        self._tail: Optional[Node[T]] = None

    @override
    def get_tail(self) -> ResultType[NodeType[T], str]:
        if not self._tail:
            return ResultType(error="Cannot retrieve the tail of the empty doubly-linked list.")

        return ResultType(value=self._tail)

    @override
    def add_to_end(self, data: Union[T, Node[T]]) -> Optional[ResultType[Node[T], str]]:
        return self.insert_node(data, -1)

    @override
    def add_to_front(self, data: Union[T, Node[T]]) -> Optional[ResultType[Node[T], str]]:
        return self.insert_node(data, 0)

    @override
    def insert_node(self, data: Union[T, Node[T]], position: int) -> Optional[ResultType[Node[T], str]]:
        return super().insert_node(data, position)

    @override
    def remove_tail(self) -> Optional[Node[T]]:
        if not (self._tail and self._head):
            raise LinkedListEmptyException("Cannot remove the tail from empty doubly-linked list.")

        # define node to remove
        node_to_remove = self._tail

        # remove from set
        self._hash_set.remove(node_to_remove)

        # arrange the linked list
        self._tail = self._tail.prev

        # clean up pointers
        node_to_remove.next = None
        node_to_remove.prev = None

        # decrease the size of linked list
        self.size -= 1

        # return the deleted tail
        return node_to_remove

    @override
    def remove_by_data(self, data: T) -> Optional[ResultType[Node[T], str]]:
        # cannot delete if empty
        if self.is_empty():
            raise LinkedListEmptyException()

        if self._head.data == data:
            # remove head
            self.remove_head()
        elif self._tail.data == data:
            # remove tail
            self.remove_tail()
        else:
            return super().remove_by_data(data)

        return None

    @override
    def display(self) -> None:
        for node in self.traverse():
            print(node, end="<-->" if node.next else "\n")

    @override
    def display_backwards(self) -> None:
        for node in self.traverse_backwards():
            print(node, end="<-->" if node.prev else "\n")

    @override
    def traverse(self) -> Iterable[Node[T]]:
        if not self._head:
            return None

        current = self._head
        while current:
            yield current
            current = current.next

    @override
    def traverse_backwards(self) -> Iterable[Node[T]]:
        if not self._tail:
            return None

        current = self._tail
        while current:
            yield current
            current = current.prev

    def traverse_forward(self) -> Iterable[Node[T]]:
        for node in self.traverse():
            yield node

    def __reversed__(self) -> Node[T]:
        for node in self.traverse_backwards():
            yield node
