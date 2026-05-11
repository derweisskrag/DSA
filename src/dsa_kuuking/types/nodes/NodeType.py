from typing import Union, TypeVar

from dsa_kuuking.types.nodes.CircularLinkedListNode import CircularLinkedListNode
from dsa_kuuking.types.nodes.DoublyLinkedListNode import DoublyLinkedListNode
from dsa_kuuking.types.nodes.LinkedListNode import LinkedListNode

# Define a type variable 'T' that is bound to the 'Node' class or its subclasses.
T = TypeVar("T", bound="NodeType")

# Define a type alias 'NodeType' that represents a node which can either be:
# - A 'DoublyLinkedListNode' instance, or
# - A 'LinkedListNode' instance.
# We would not use this one for now
# Because we match the type of the linked list to determine whether to create a singly or doubly linked node, we can just use the 'Node' class as the base type for our nodes.
NodeType = Union[CircularLinkedListNode, DoublyLinkedListNode[T], LinkedListNode[T]]

