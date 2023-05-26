from types import MethodType
from src.sosecrets.exceptions import CannotInheritFromSecret, FuncAndValueCannotBeBothPassed, CannotInstantiateExposeSecret
from src.sosecrets.typed import SecretType, T, Generic, Callable, Any, Tuple, Dict, Optional


class __expose_secret__:

    def __init__(self):
        raise CannotInstantiateExposeSecret

    def __call__(self,
                 value: Optional[T] = None,
                 /,
                 func: Optional[Callable[[Any],
                                T]] = None,
                 func_args: Tuple[Any] = tuple(),
                 func_kwargs: Dict[str,
                                   Any] = dict()):

        if func is not None and value is not None:
            raise FuncAndValueCannotBeBothPassed
        if func is not None:
            value = func(*func_args, **func_kwargs)

        def wrapper(slf):
            return value
        return wrapper


class SecretMeta(type):
    def __call__(cls,
                 value: Optional[T] = None,
                 /,
                 func: Optional[Callable[[Any],
                                T]] = None,
                 func_args: Tuple[Any] = tuple(),
                 func_kwargs: Dict[str,
                                   Any] = dict()):

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

    __slots__ = ('expose_secret')

    def apply(self, func: Callable[[Any], Any],
              *args: Tuple[Any], **kwargs: Dict[str, Any]) -> SecretType:
        return Secret(func(self.expose_secret(), *args, **kwargs))

    def __enter__(self) -> T:
        return self.expose_secret()

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        ...

    def __init_subclass__(cls, **init_sc_kwargs) -> None:
        raise CannotInheritFromSecret
