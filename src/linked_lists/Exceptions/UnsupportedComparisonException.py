class UnsupportedComparisonException(Exception):
    """
    Raised when a type does not support comparison operations.

    Attributes:
        message (str): A message describing the exception.
    """

    def __init__(self, message: str = "The data type does not support comparison operations.") -> None:
        self.message = message
        super().__init__(self.message)