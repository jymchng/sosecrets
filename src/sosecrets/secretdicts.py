from collections import UserDict
from sosecrets_core.secrets import Secret
from typing import Dict, Any, Optional, Callable, Tuple, Mapping


class ImmutableSecretMapping(UserDict, Mapping[Any, Secret]):
    """
    A dictionary-like object that stores secret values and prevents changes to the dictionary.
    """
    _frozen = False
    
    def __init__(self, dict=None, /, **kwargs):
        """
        Initialize a new `ImmutableSecretMapping` object.

        Args:
            mapping (Dict[Any, Any]): A dictionary with `Any` keys and `Any` values.
        """
        if dict is None or dict == {}:
            raise ValueError("Cannot initialize `ImmutableSecretMapping` with an empty dictionary")
        super().__init__(dict, **kwargs)
        for k, v in self.data.items():
            if not isinstance(v, Secret):
                self.data[k] = Secret(v)
            else:
                self.data[k] = v
        self._frozen = True

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Raise an exception when attempting to set a new key-value pair in the `ImmutableSecretMapping` object.

        Parameters:
            key (Any): The key to set.
            value (Any): The value to set.

        Raises:
            TypeError: When attempting to set a new key-value pair.
        """
        if self._frozen:
            raise TypeError(
                "ImmutableSecretMapping object does not support item assignment.")
        super().__setitem__(key, value)

    @classmethod
    def from_func(
            cls,
            func: Callable[[Any], Dict[Any, Any]],
            *func_args: Tuple[Any],
            **func_kwargs: Dict[Any, Any]) -> 'ImmutableSecretMapping':
        """Create a new ImmutableSecretMapping object from the result of a function.

        Args:
            func (callable): A function that returns a dictionary with `Any` keys and secret values.
            *func_args (Any): Positional arguments to pass to the function.
            **func_kwargs (Any): Keyword arguments to pass to the function.

        Returns:
            ImmutableSecretMapping: A new ImmutableSecretMapping object.

        Raises:
            ValueError: If the result of the function is empty.
        """
        mapping = func(*func_args, **func_kwargs)
        if not mapping:
            raise ValueError("Result of the function is empty.")
        new_mapping = {}
        for k, v in mapping.items():
            if not isinstance(v, Secret):
                new_mapping[k] = Secret(v)
            else:
                new_mapping[k] = v
        return cls(new_mapping)

    def get_exposed(self, key: Any, default: Optional[Any] = None) -> Any:
        """Get the exposed value of a key in the ImmutableSecretMapping object.

        Args:
            key (Any): The key to get.
            default (Optional[Any]): The default value to return if the key is not found.

        Returns:
            Any: The exposed value of the key, or the default value if the key is not found."""
        value: Secret = self.data.get(key, default)
        if value == default:
            return value
        return value.expose_secret()

    def expose_dict(self) -> Dict[Any, Any]:
        """
        Return a new dictionary that exposes exposed information.

        This method returns a new dictionary with the same keys as the original dictionary,
        but with values that have been converted to exposed information using their `expose_secret()` method.
        The `expose_secret()` method is expected to return a exposed version of the value.

        Returns:
            Dict[Any, Any]: A new dictionary with exposed values.
        """
        return {k: v.expose_secret() for k, v in self.data.items()}


class MutableSecretMapping(UserDict, Mapping[Any, Secret]):
    """
    A dictionary-like object that stores secret values and allows changes to the dictionary.
    """
    _unset = True
    
    def __init__(self, dict=None, /, **kwargs):
        """
        Initialize a new `MutableSecretMapping` object.

        Args:
            mapping (Dict[Any, Any]): A dictionary with `Any` keys and `Any` values.
        """
        super().__init__(dict, **kwargs)
        for k, v in self.data.items():
            if not isinstance(v, Secret):
                self.data[k] = Secret(v)
            else:
                self.data[k] = v
        self._unset = False

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set a new key-value pair in the `MutableSecretMapping` object.

        Parameters:
            key (Any): The key to set.
            value (Any): The value to set.

        Raises:
            ValueError: If the value is not of type `Secret`.
        """
        if self._unset:
            if not isinstance(value, Secret):
                value = Secret(value)
            super().__setitem__(key, value)
        if not isinstance(value, Secret):
            raise ValueError("Value must be of type `Secret`.")
        super().__setitem__(key, value)
        

    @classmethod
    def from_func(
            cls,
            func: Callable[..., Dict[Any, Any]],
            *func_args: Tuple[Any, ...],
            **func_kwargs: Dict[Any, Any]) -> 'MutableSecretMapping':
        """Create a new `MutableSecretMapping` object from the result of a function.

        Args:
            func (callable): A function that returns a dictionary with `Any` keys and secret values.
            *func_args (Any): Positional arguments to pass to the function.
            **func_kwargs (Any): Keyword arguments to pass to the function.

        Returns:
            MutableSecretMapping: A new `MutableSecretMapping` object.

        Raises:
            ValueError: If the result of the function is empty.
        """
        mapping = func(*func_args, **func_kwargs)
        if not mapping:
            raise ValueError("Result of the function is empty.")
        new_mapping = {}
        for k, v in mapping.items():
            if not isinstance(v, Secret):
                new_mapping[k] = Secret(v)
            else:
                new_mapping[k] = v
        return cls(new_mapping)

    def get_exposed(self, key: Any, default: Optional[Any] = None) -> Any:
        """
        Get the exposed value of a key in the `MutableSecretMapping` object.

        Args:
            key (Any): The key to get.
            default (Optional[Any]): The default value to return if the key is not found.

        Returns:
            Any: The exposed value of the key, or the default value if the key is not found.
        """
        value: Secret = super().get(key, default)
        if value == default:
            return value
        return value.expose_secret()

    def expose_dict(self) -> Dict[Any, Any]:
        """
        Return a new dictionary that exposes exposed information.

        This method returns a new dictionary with the same keys as the original dictionary,
        but with values that have been converted to exposed information using their `expose_secret()` method.
        The `expose_secret()` method is expected to return a exposed version of the value.

        Returns:
            Dict[Any, Any]: A new dictionary with exposed values.
        """
        return {k: v.expose_secret() for k, v in super().items()}
