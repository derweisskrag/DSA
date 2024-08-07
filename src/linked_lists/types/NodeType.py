from typing import Union, TypeVar

from src.linked_lists.types.CircularLinkedListNode import CircularLinkedListNode
from src.linked_lists.types.DoublyLinkedListNode import DoublyLinkedListNode
from src.linked_lists.types.LinkedListNode import LinkedListNode

# Define a type variable 'T' that is bound to the 'Node' class or its subclasses.
T = TypeVar("T", bound="Node")

# Define a type alias 'NodeType' that represents a node which can either be:
# - A 'DoublyLinkedListNode' instance, or
# - A 'LinkedListNode' instance.
NodeType = Union[CircularLinkedListNode, DoublyLinkedListNode[T], LinkedListNode[T]]

