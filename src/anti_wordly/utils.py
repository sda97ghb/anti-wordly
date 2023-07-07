from typing import TypeVar
from collections.abc import Iterable

T = TypeVar("T")


def first(iterable: Iterable[T]) -> T:
    return next(iter(iterable))


def first_n(iterable: Iterable[T], n: int) -> Iterable[T]:
    for idx, item in enumerate(iterable):
        if idx >= n:
            return
        yield item
