from typing import Union, TypeVar

from src.types.nodes.CircularLinkedListNode import CircularLinkedListNode
from src.types.nodes.DoublyLinkedListNode import DoublyLinkedListNode
from src.types.nodes.LinkedListNode import LinkedListNode

# Define a type variable 'T' that is bound to the 'Node' class or its subclasses.
T = TypeVar("T", bound="Node")

# Define a type alias 'NodeType' that represents a node which can either be:
# - A 'DoublyLinkedListNode' instance, or
# - A 'LinkedListNode' instance.
NodeType = Union[CircularLinkedListNode, DoublyLinkedListNode[T], LinkedListNode[T]]

