

class LinkedListEmptyException(Exception):
    """
    Exception raised  when an operation is attempted on an empty LinkedList.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self,
                 message: str = "The LinkedList is empty! Cannot delete non-existing elements in the list.") -> None:
        self.message = message

        super().__init__(self.message)
