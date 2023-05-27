from types import MethodType
from src.sosecrets.exceptions import CannotInheritFromSecret, FuncAndValueCannotBeBothPassed, CannotInstantiateExposeSecret
from typing import Generic, Callable, Any, Tuple, Dict, Optional, TypeVar


T = TypeVar('T', covariant=True)


class __expose_secret__:
    """
    Helper class to encapsulate the `expose_secret` method of the `Secret` class.

    This class is used to prevent direct instantiation of the `expose_secret` method.
    """

    def __init__(self):
        raise CannotInstantiateExposeSecret

    def __call__(self,
                 value: Optional[T] = None,
                 /,
                 func: Optional[Callable[[Any],
                                T]] = None,
                 func_args: Tuple[Any] = (),
                 func_kwargs: Dict[str, Any] = {}):

        if func is not None and value is not None:
            raise FuncAndValueCannotBeBothPassed
        if func is not None:
            value = func(*func_args, **func_kwargs)

        def wrapper(slf) -> T:
            """
            Returns the secret value.

            Returns:
                The secret value.
            """
            return value
        return wrapper


class SecretMeta(type):
    """
    Metaclass for the `Secret` class.

    This metaclass customizes the instantiation of `Secret` objects and ensures that the `expose_secret` method is properly
    initialized with an instance of `__expose_secret__`.
    """

    def __call__(cls,
                 value: Optional[T] = None,
                 /,
                 func: Optional[Callable[[Any],
                                T]] = None,
                 func_args: Tuple[Any] = (),
                 func_kwargs: Dict[str, Any] = {}) -> 'Secret':
        obj = object.__new__(Secret)
        new_func_obj = object.__new__(__expose_secret__)
        obj.expose_secret = MethodType(
            new_func_obj(
                value,
                func=func,
                func_args=func_args,
                func_kwargs=func_kwargs),
            obj)
        return obj


class Secret(Generic[T], metaclass=SecretMeta):
    """
    A class that encapsulates a secret value and provides a controlled interface for accessing it.
    """

    __slots__ = ('expose_secret',)

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
        return Secret(func(self.expose_secret(), *args, **kwargs))

    def __enter__(self) -> T:
        return self.expose_secret()

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        return None

    def __init_subclass__(cls, **init_sc_kwargs) -> None:
        raise CannotInheritFromSecret
