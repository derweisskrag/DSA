from abc import ABC, abstractmethod
from typing import Optional, Union

from src.trees.types.red_black_tree_node import Node, NIL


class RBTreeInterface[T](ABC):
    @abstractmethod
    def add(self, key: T, value: T) -> None: ...

    @abstractmethod
    def remove(self, key: T) -> Optional[Node[T]]: ...

    @abstractmethod
    def swap(self, u: Node[T], v: Node[T]) -> None: ...

    @abstractmethod
    def is_empty(self) -> bool: ...

    @abstractmethod
    def get_node_or_mock(self, node: Node[T]) -> Optional[Union[NIL, Node[T]]]: ...

    @abstractmethod
    def find_by_key(self, key: T) -> Optional[Node[T]]: ...

    @abstractmethod
    def count_children(self, node: Node[T]) -> int: ...

    @staticmethod
    @abstractmethod
    def node_exists(node: Union[NIL, Node[T]]) -> bool: ...

    @staticmethod
    @abstractmethod
    def is_leaf(node: Union[Node[T], NIL]) -> bool: ...

    @abstractmethod
    def predecessor(self, node: Union[NIL, Node[T]]) -> Node[T]: ...

    @abstractmethod
    def successor(self, node: Union[NIL, Node[T]]) -> Node[T]: ...

    @abstractmethod
    def in_order_traverse(self, node: Node[T]) -> None: ...

    @abstractmethod
    def pre_order_traverse(self, node: Node[T]) -> None: ...

    @abstractmethod
    def post_order_traverse(self, node: Node[T]) -> None: ...

