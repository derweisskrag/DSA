class EmptyQueueException(Exception):
    def __init__(self, message: str = "Empty Queue!"):
        super().__init__(message)
