"""This module contains the definition of the linked list"""


from abc import abstractmethod, ABC
from typing import Optional, Iterable, Dict, Union
from src.linked_lists.types.NodeType import NodeType
from src.linked_lists.types.ResultType import ResultType


class LinkedListInterface[T](ABC):
    """The interface for linked list"""
    @abstractmethod
    def add_to_front(self, data: Union[T, NodeType[T]]) -> Optional[ResultType[NodeType[T], str]]: ...

    @abstractmethod
    def insert_node(self, data: Union[T, NodeType[T]], position: int) -> Optional[ResultType[NodeType[T], str]]: ...

    @abstractmethod
    def remove_by_id(self, node_id: int) -> Optional[NodeType[T]]: ...

    @abstractmethod
    def remove_by_data(self, data: T) -> Optional[NodeType[T]]: ...

    @abstractmethod
    def remove_head(self) -> Optional[NodeType[T]]: ...

    @abstractmethod
    def find_spot(self, target: NodeType[T]) -> Optional[NodeType[T]]: ...

    @abstractmethod
    def find_by_id(self, node_id: int) -> Optional[NodeType[T]]: ...

    @abstractmethod
    def find_by_data(self, data: T) -> Optional[NodeType[T]]: ...

    @abstractmethod
    def find_by_params(self, search_param: Dict[str, Union[str, int, float]]) -> Optional[NodeType[T]]: ...

    @abstractmethod
    def find_by_attribute(self, attribute_name: str, attribute_value: Union[str, int]) -> Optional[NodeType[T]]: ...

    @abstractmethod
    def is_empty(self) -> bool: ...

    @abstractmethod
    def get_head(self) -> ResultType[NodeType[T], str]: ...

    @abstractmethod
    def display(self) -> None: ...

    @abstractmethod
    def display_backwards(self) -> None: ...

    @abstractmethod
    def get_size(self) -> int: ...

    @abstractmethod
    def traverse(self) -> Iterable[NodeType[T]]: ...

    @abstractmethod
    def traverse_backwards(self) -> Iterable[NodeType[T]]: ...

    @abstractmethod
    def swap_two_nodes(self, a: NodeType[T], b: NodeType[T]) -> None: ...
