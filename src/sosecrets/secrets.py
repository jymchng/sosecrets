from types import MethodType
from src.sosecrets.exceptions import CannotInheritFromSecret, FuncAndValueCannotBeBothPassed, CannotInstantiateExposeSecret
from src.sosecrets.typed import SecretType


class __inner_secret__:
    __slots__ = ('expose_secret')

    def apply(self, func, *args, **kwargs):
        return Secret(func(self.expose_secret(), *args, **kwargs))

    def __enter__(self):
        return self.expose_secret()

    def __exit__(self, exc_type, exc_value, exc_tb):
        ...


class __expose_secret__:

    def __init__(self):
        raise CannotInstantiateExposeSecret

    def __call__(self, value, /, func=None, func_args=(), func_kwargs={}):
        if func is not None and value is not None:
            raise FuncAndValueCannotBeBothPassed
        if func is not None:
            value = func(*func_args, **func_kwargs)

        def wrapper(slf):
            return value
        return wrapper


class SecretMeta(type):
    def __call__(cls, value=None, /, func=None, func_args=(), func_kwargs={}):
        obj = object.__new__(__inner_secret__)
        new_func_obj = object.__new__(__expose_secret__)
        obj.expose_secret = MethodType(
            new_func_obj(
                value,
                func=func,
                func_args=func_args,
                func_kwargs=func_kwargs),
            obj)
        return obj

    def __instancecheck__(self, inst):
        return isinstance(inst, __inner_secret__)


class Secret(metaclass=SecretMeta):

    def __init_subclass__(cls, **init_sc_kwargs):
        raise CannotInheritFromSecret
