from typing import List


class TrashContainer[T]:
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.stack: List[T] = []

    def add_trash(self): ...

    def empty_trash_container(self): ...

    def schedule(self): ...