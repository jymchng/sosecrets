from typing import Generic, TypeVar, Callable, Any, Tuple, Dict

T = TypeVar('T')


class SecretType(Generic[T]):

    def expose_secret(self) -> T:
        ...

    def __init__(self, value: T, /, * \
                 args: Tuple[Any], func: Callable[[Any], T], **kwargs: Dict[Any, Any]):
        ...
