from types import MethodType
from src.sosecrets.exceptions import CannotInheritFromSecret, FuncAndValueCannotBeBothPassed, CannotInstantiateExposeSecret
from src.sosecrets.typed import SecretType, T, Generic, Callable, Any, Tuple, Dict, Optional


class __expose_secret__:
    """
    Helper class to encapsulate the `expose_secret` method of the `Secret` class.

    This class is used to prevent direct instantiation of the `expose_secret` method.
    """

    def __init__(self):
        """
        Raises:
            CannotInstantiateExposeSecret: This class cannot be instantiated directly.
        """
        raise CannotInstantiateExposeSecret

    def __call__(self,
                 value: Optional[T] = None,
                 /,
                 func: Optional[Callable[[Any],
                                T]] = None,
                 func_args: Tuple[Any] = (),
                 func_kwargs: Dict[str, Any] = {}):
        """
        Returns a function that returns the secret value.

        Args:
            value: The secret value to encapsulate.
            func: A function to generate the secret value.
            func_args: The positional arguments to pass to the `func` function.
            func_kwargs: The keyword arguments to pass to the `func` function.

        Raises:
            FuncAndValueCannotBeBothPassed: Both `value` and `func`arguments cannot be passed at the same time.

        Returns:
            A function that returns the secret value.
        """

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
        """
        Creates a new `Secret` object with the specified value or function.

        Args:
            value: The secret value to encapsulate.
            func: A function to generate the secret value.
            func_args: The positional arguments to pass to the `func` function.
            func_kwargs: The keyword arguments to pass to the `func` function.

        Returns:
            A new `Secret` object with thespecified value or function.
        """
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

    This class provides the `apply` method to apply a function to the secret value while keeping it encapsulated. It also
    provides the `__enter__` and `__exit__` methods to support the use of `Secret` objects as context managers.
    """

    __slots__ = ('expose_secret',)

    def apply(self, func: Callable[[T, Any], Any],
              *args: Tuple[Any], **kwargs: Dict[str, Any]) -> SecretType:
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
        """
        Returns the value of the secret.

        This method allows `Secret` objects to be used as context managers.

        Returns:
            The value of the secret.
        """
        return self.expose_secret()

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        """
        Placeholder method for use of `Secret` objects as context managers.

        This method is currently not used and simply returns `None`.

        Args:
            exc_type: The type of the exception (if any) that was raised.
            exc_value: The value of the exception (if any) that was raised.
            exc_tb: The traceback of the exception (if any) that was raised.
        """
        return None

    def __init_subclass__(cls, **init_sc_kwargs) -> None:
        """
        Raises an exception to prevent subclassing of the `Secret` class.
        """
        raise CannotInheritFromSecret
