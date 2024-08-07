from typing import Optional, final

from src.linked_lists.types.LinkedListNode import LinkedListNode


@final
class DoublyLinkedListNode[T](LinkedListNode):
    def __init__(self, data: T) -> None:
        super().__init__(data)
        self.prev: Optional['DoublyLinkedListNode[T]'] = None
