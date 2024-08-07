class NodeNotFoundException(Exception):
    """
    Exception raised when a node with the specified data is not found in the LinkedList.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message: str = "Node with the specified data not found in the LinkedList.") -> None:
        self.message = message
        super().__init__(self.message)