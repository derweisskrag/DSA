class DataclassNotUsedException(Exception):
    """
    Raised when a class used in comparison does not meet the expected criteria,
    such as not being a dataclass or not implementing the necessary methods for comparison.

    Attributes:
        message (str): A message describing the exception.
    """

    def __init__(self, message: str = "The class being used does not meet the expected criteria.") -> None:
        self.message = message
        super().__init__(self.message)