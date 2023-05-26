from typing import Generic, TypeVar, Callable, Any, Tuple, Dict, Optional, Union

T = TypeVar('T')


class SecretType(Generic[T]):

    def expose_secret(self) -> T:
        ...

    def __init__(self,
                 value: Optional[T] = None,
                 /,
                 func: Optional[Callable[[Any],
                                T]] = None,
                 func_args: Union[Tuple[Any], Tuple] = tuple(),
                 func_kwargs: Dict[str,
                                   Any] = dict()):
        ...
