from typing import final, Optional

from src.types.nodes.LinkedListNode import LinkedListNode


@final
class CircularLinkedListNode[T](LinkedListNode):
    def __init__(self, data: T) -> None:
        super().__init__(data)
        self.prev: Optional['CircularLinkedListNode'] = None
