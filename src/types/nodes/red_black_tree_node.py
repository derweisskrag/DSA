from typing import Optional

from src.types.enums.rbtree_colours import Color


class NIL:
    def __init__(self) -> None:
        self.key = None
        self.value = None

        # pointers
        self.left = self
        self.right = self
        self.parent = None

        # color
        self.color = Color.BLACK

    def __str__(self) -> str:
        return f"NIL"


class Node[T]:
    def __init__(self, key: T, value: T, color: Optional[Color] = Color.RED) -> None:
        # assign values
        self.key = key
        self.value = value

        # check for the values
        assert key is not None, f"Key cannot be None: {key}"
        assert value is not None, f"Value cannot be None: {value}"

        # assign pointers
        self.left = NIL()
        self.right = NIL()
        self.parent = None  # parent is None, not NIL

        # colour is always RED
        self.color = color

    def __str__(self) -> str:
        return f"Node(key={self.key}, value={self.value}, color={self.color})"