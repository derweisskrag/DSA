class AttributeNotFoundException(Exception):
    """
    Exception raised when the attribute is not found in the node data.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, attribute: str, message: str = None):
        self.attribute = attribute
        self.message = message or f"Attribute '{attribute}' not found in the node data."
        super().__init__(self.message)
