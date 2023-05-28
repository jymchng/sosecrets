from typing import Generic, TypeVar, Callable, Any, Tuple, Dict, Optional, Union

T = TypeVar('T')


class Secret(Generic[T]):
    """
    A class that encapsulates a secret value and provides a controlled interface for accessing it.
    """

    def expose_secret(self) -> T:
        "Exposes the hidden secret."
        ...

    def __init__(self,
                 value: Optional[T] = None,
                 /,
                 func: Optional[Callable[[Any],
                                T]] = None,
                 func_args: Union[Tuple[Any], Tuple] = tuple(),
                 func_kwargs: Dict[str,
                                   Any] = dict()) -> 'Secret':
        ...

    def apply(self, func: Callable[[T, Any], Any],
              *args: Tuple[Any], **kwargs: Dict[str, Any]) -> 'Secret':
        """
        Applies a function to the secret value while keeping it encapsulated.

        Args:
            func: The function to apply to the secret value.
            args: The positional arguments to pass to the `func` function.
            kwargs: The keyword arguments to pass to the `func` function.

        Returns:
            A new `Secret` object encapsulating the result of applying `func` to the secret value.
        """
        ...
