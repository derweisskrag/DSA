from abc import ABC, abstractmethod

from src.linked_lists.interfaces.linked_list_interface import LinkedListInterface


class CircularLinkedListInterface[T](LinkedListInterface, ABC):
    @abstractmethod
    def balance_list(self): ...
