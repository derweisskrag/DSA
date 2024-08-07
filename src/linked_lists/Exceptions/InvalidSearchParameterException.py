class InvalidSearchParameterException(Exception):
    """
    Exception raised for errors in the search parameter format.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self,
                 message: str = "Invalid search parameter. Must be a dictionary with exactly one key-value pair.") -> None:
        self.message = message
        super().__init__(self.message)
