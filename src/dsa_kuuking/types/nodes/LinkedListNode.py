"""This module contains the type for Node used by linked lists classes"""

from typing import Optional


class LinkedListNode[T]:
    """A node in a linked list."""
    __slots__ = ['_data', 'next', '_id']
    def __init__(self, data: T):
        self._data = data
        self.next: Optional['LinkedListNode[T]'] = None
        self._id = id(self)

    @property
    def data(self) -> T:
        """Getter method for the data."""
        return self._data

    def get_id(self) -> int:
        """Retrieves the id of a node"""
        return self._id

    def __repr__(self):
        return f"Node(data={self.data})"

    def __eq__(self, other):
        if not isinstance(other, LinkedListNode):
            return self.data == other # handle the scalar
        # Alternative to checking by data is just using data
        # use IS
        return self is other # and self.get_id() == other.get_id()

