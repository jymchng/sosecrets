from typing import Callable, Optional, Any, Dict, Tuple, ClassVar, TypeVar, Generic

T = TypeVar('T')

class Secret(Generic[T]):
    """The Secret class is a Python class that encapsulates a secret value and provides methods to access it.
    The secret value can be initialized either with a direct value or with a function that generates the value.
    The class allows for limiting the number of times the secret value can be exposed.

    The `expose_secret()` method returns the inner secret value and increments the exposure count, `expose_count`.
    If the exposure count, `expose_count` is larger than the maximum exposure count, `max_expose_count`, an AttributeError is raised.
    
    The `apply()` method applies a function to the inner secret value and returns a new Secret object with the result encapsulated within.
    The original Secret object is not modified.

    This class provides a way to control access to sensitive data by encapsulating it within a class and allowing access only through well-defined methods.
    This can help prevent accidental exposure of sensitive data as much as possible.
    """
    expose_count: ClassVar[int]
    max_expose_count: ClassVar[int]

    def __init__(
        self,
        value: Optional[T] = ...,
        *,
        func: Optional[Callable[..., T]] = ...,
        func_args: Tuple[Any, ...] = ...,
        func_kwargs: Dict[str, Any] = ...,
        max_expose_count: int = ...,
    ) -> None:
        """
        Initialize a Secret object.

        Args:
            value: The initial value of the Secret object. If provided, it takes precedence over `func`.
            func: A function used to generate the initial value of the Secret object. Ignored if `value` is provided.
            func_args: Positional arguments to pass to the `func` function. Ignored if `value` is provided.
            func_kwargs: Keyword arguments to pass to the `func` function. Ignored if `value` is provided.
            max_expose_count: The maximum number of times the Secret object can be exposed. Set to -1 for unlimited.

        Raises:
            ValueError: If both `value` and `func` arguments are provided.

        """
        ...

    def expose_secret(self) -> T:
        """
        Expose the secret value.

        Returns:
            The inner secret value.

        Raises:
            AttributeError: If the Secret object has reached the maximum exposure count.

        """
        ...

    def apply(
        self,
        func: Callable[..., Any],
        *,
        func_args: Tuple[Any, ...] = ...,
        func_kwargs: Dict[str, Any] = ...,
    ) -> 'Secret':
        """
        Apply a function to the inner secret value and return a new Secret object.

        Args:
            func: The function to apply to the inner secret value.
            func_args: Positional arguments to pass to the `func` function.
            func_kwargs: Keyword arguments to pass to the `func` function.

        Returns:
            A new Secret object with the result of applying the function to the inner secret value.

        """
        ...
