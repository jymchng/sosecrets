from src.sosecrets.secrets import Secret, Dict, Any, Optional


class ImmutableSecretMapping(dict, Dict[Any, Secret]):
    """
    A dictionary-like object that stores secret values and prevents changes to the dictionary.
    """
    def __new__(cls, mapping: Dict[Any, Any]):
        """
        Initialize the ImmutableSecretMapping object.

        Parameters:
        - mapping (Dict[Any, Any]): A dictionary with `Any` keys and secret values.

       Raises:
        - Exception: If the mapping argument is empty or if any of the values in the mapping are not of type Secret.
        """
        if not mapping:
            raise ValueError("Mapping argument is empty.")
        new_mapping = {}
        for k, v in mapping.items():
            if not isinstance(v, Secret):
                new_mapping[k] = Secret(v)
            else:
                new_mapping[k] = v
        return super().__new__(cls, new_mapping)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Raise an exception when attempting to set a new key-value pair in the `ImmutableSecretMapping` object.

        Parameters:
        - key (Any): The key to set.
        - value (Any): The value to set.

        Raises:
        - Exception: When attempting to set a new key-value pair.
        """
        raise TypeError(
            "ImmutableSecretMapping object does not support item assignment.")

    @classmethod
    def from_func(
            cls,
            func,
            *func_args,
            **func_kwargs) -> 'ImmutableSecretMapping':
        """
        Create a new ImmutableSecretMapping object from the result of a function.

        Parameters:
        - func (callable): A function that returns a dictionary with Anying keys and secret values.
        - *func_args (Any): Positional arguments to pass to the function.
        - **func_kwargs (Any): Keyword arguments to pass to the function.

        Returns:
        - ImmutableSecretMapping: A new ImmutableSecretMapping object.

       Raises:
        - ValueError: If the result of the function is empty or if any of the values in the result are not of type Secret.
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
        Get the exposed value of a key in the ImmutableSecretMapping object.

        Parameters:
        - key (Any): The key to get.
        - default (Optional[Any]): The default value to return if the key is not found.

        Returns:
        - Any: The exposed value of the key, or the default value if the key is not found.
        """
        value = super().get(key, default)
        if value == default:
            return value
        return value.expose_secret()

    def expose_dict(self) -> Dict[Any, Any]:
        """
        Return a new dictionary that exposes non-sensitive information.

        This method returns a new dictionary with the same keys as the original dictionary, but with values that have been converted to non-sensitive information using their `expose_secret()` method. The `expose_secret()` method is expected to return a non-sensitive version of the value, so that the dictionary can be safely exported or displayed without exposing sensitive information.

        Returns:
            A new dictionary with non-sensitive values.
        """
        return {k: v.expose_secret() for k, v in super().items()}


class MutableSecretMapping(dict):
    """
    A dictionary-like object that stores secret values and allows changes to the dictionary.
    """
    def __new__(cls, mapping: Dict[Any, Any]):
        """
        Initialize the MutableSecretMapping object.

        Parameters:
        - mapping (Dict[Any, Any]): A dictionary with Any keys and secret values.

        Raises:
        - ValueError: If the mapping argument is empty or if any of the values in the mapping are not of type Secret.
        """
        if not mapping:
            raise ValueError("Mapping argument is empty.")
        new_mapping = {}
        for k, v in mapping.items():
            if not isinstance(v, Secret):
                new_mapping[k] = Secret(v)
            else:
                new_mapping[k] = v
        return super().__new__(cls, new_mapping)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set a new key-value pair in the MutableSecretMapping object.

        Parameters:
        - key (Any): The key to set.
        - value (Any): The value to set.

        Raises:
        - ValueError: If the value is not of type Secret.
        """
        if not isinstance(value, Secret):
            raise ValueError("Value must be of type Secret.")
        super().__setitem__(key, value)

    @classmethod
    def from_func(
            cls,
            func,
            *func_args,
            **func_kwargs) -> 'MutableSecretMapping':
        """
        Create a new MutableSecretMapping object from the result of a function.

        Parameters:
        - func (callable): A function that returns a dictionary with `Any` keys and secret values.
        - *func_args (Any): Positional arguments to pass to the function.
        - **func_kwargs (Any): Keyword arguments to pass to the function.

        Returns:
        - MutableSecretMapping: A new MutableSecretMapping object.

        Raises:
        - ValueError: If the result of the function is empty or if any of the values in the result are not of type Secret.
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
        Get the exposed value of a key in the MutableSecretMapping object.

        Parameters:
        - key (Any): The key to get.
        - default (Optional[Any]): The default value to return if the key is not found.

        Returns:
        - Any: The exposed value of the key, or the default value if the key is not found.
        """
        return super().get(key, default).expose_secret()

    def expose_dict(self) -> Dict[Any, Any]:
        """
        Return a new dictionary that exposes non-sensitive information.

        This method returns a new dictionary with the same keys as the original dictionary, but with values that have been converted to non-sensitive information using their `expose_secret()` method. The `expose_secret()` method is expected to return a non-sensitive version of the value, so that the dictionary can be safely exported or displayed without exposing sensitive information.

        Returns:
            A new dictionary with non-sensitive values.
        """
        return {k: v.expose_secret() for k, v in super().items()}
