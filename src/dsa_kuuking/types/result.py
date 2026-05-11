from typing import TypeVar, Generic, Optional, Callable, Any
from functools import wraps

T = TypeVar("T")
E = TypeVar("E")

class Result(Generic[T, E]):
    __slots__ = ("_value", "_error")

    def __init__(self, value: Optional[T] = None, error: Optional[E] = None):
        self._value = value
        self._error = error

    def is_ok(self) -> bool:
        return self._error is None

    def is_err(self) -> bool:
        return self._error is not None

    def unwrap(self) -> T:
        if self.is_err():
            raise Exception(self._error)
        return self._value  # type: ignore

    def unwrap_or(self, default_value: T) -> T:
        return self._value if self.is_ok() else default_value  # type: ignore

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return self._value if self.is_ok() else func()  # type: ignore

    def expect(self, msg: str) -> T:
        if self.is_err():
            raise Exception(f"{msg}: {self._error}")
        return self._value  # type: ignore

    def map(self, func: Callable[[T], Any]) -> "Result[Any, E]":
        if self.is_ok():
            try:
                return Ok(func(self._value))  # type: ignore
            except Exception as e:
                return Err(e)
        return Err(self._error)  # type: ignore

    def and_then(self, func: Callable[[T], "Result[Any, E]"]) -> "Result[Any, E]":
        if self.is_ok():
            try:
                res = func(self._value)  # type: ignore
                return res if isinstance(res, Result) else Ok(res)
            except Exception as e:
                return Err(e)
        return Err(self._error)  # type: ignore

    def __repr__(self) -> str:
        return f"Ok({self._value})" if self.is_ok() else f"Err({self._error})"

class Ok(Result[T, None]):
    __slots__ = ()
    def __init__(self, value: T) -> None:
        super().__init__(value=value)

class Err(Result[None, E]):
    __slots__ = ()
    def __init__(self, error: E) -> None:
        super().__init__(error=error)

def result_wrapper(func: Callable[..., T]) -> Callable[..., Result[T, Exception]]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Result[T, Exception]:
        try:
            res = func(*args, **kwargs)
            return res if isinstance(res, Result) else Ok(res)
        except Exception as e:
            return Err(e)
    return wrapper