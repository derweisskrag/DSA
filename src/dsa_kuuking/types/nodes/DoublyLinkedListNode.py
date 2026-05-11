from typing import Optional, final

from dsa_kuuking.types.nodes.LinkedListNode import LinkedListNode


@final
class DoublyLinkedListNode[T](LinkedListNode):
    """A node in a doubly linked list."""
    __slots__ = ['prev']
    def __init__(self, data: T) -> None:
        super().__init__(data)
        self.prev: Optional['DoublyLinkedListNode[T]'] = None
