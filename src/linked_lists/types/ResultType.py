from typing import Optional


class ResultType[T, E]:
    def __init__(self, value: Optional[T] = None, error: Optional[E] = None) -> None:
        self.value = value
        self.error = error

    def is_ok(self):
        return self.error is None

    def is_err(self):
        return self.error is not None

    def unwrap(self) -> T:
        if self.is_err():
            raise ValueError(f"Called unwrap on an error result: {self.error}")
        return self.value

    def unwrap_err(self) -> E:
        if self.is_ok():
            raise ValueError(f"Called unwrap_err on an ok result: {self.value}")
        return self.error
