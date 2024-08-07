class SizeManagementException(Exception):
    def __init__(self, message: str = "Size management exception"):
        super().__init__(message)