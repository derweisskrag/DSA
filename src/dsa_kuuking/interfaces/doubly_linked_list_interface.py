from abc import ABC, abstractmethod
from typing import Optional, Iterable

from dsa_kuuking.interfaces.linked_list_interface import LinkedListInterface
from dsa_kuuking.types.nodes.NodeType import NodeType
from dsa_kuuking.types.ResultType import ResultType


class DoublyLinkedListInterface[T](LinkedListInterface, ABC):
    @abstractmethod
    def add_to_end(self, data: T) -> Optional[ResultType[NodeType[T], str]]: ...

    @abstractmethod
    def remove_tail(self) -> Optional[ResultType[NodeType[T], str]]: ...

    @abstractmethod
    def traverse_backwards(self) -> Iterable[NodeType[T]]: ...

    @abstractmethod
    def get_tail(self) -> ResultType[NodeType[T], str]: ...
