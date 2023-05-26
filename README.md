# sosecrets

`sosecrets` is a Python module that provides a secure way to handle sensitive data by encapsulating it and only exposing it through a controlled interface.

## Installation

To install `sosecrets`, you can use pip:

```bash
pip install sosecrets
```

## Usage

Here's an example of how to use `sosecrets`:

```python
from sosecrets import Secret

# Create a secret value
secret_value = Secret("my secret value")

# Use the secret value while keeping it encapsulated
result = secret_value.apply(len)
print(result)  # Output: 14

# Get the value of the secret
value = secret_value.expose_secret()
print(value)  # Output: "my secret value"
```

In this example, we create a `Secret` object with the value "my secret value". We then use the `apply` method to apply the `len` function to the secret value while keeping it encapsulated. Finally, we use the `expose_secret` method to retrieve the value of the secret.

## Use Cases
sosecrets can be used in a variety of scenarios where sensitive data needs to be securely handled. Here are some common use cases:

Storing API keys, passwords, and other credentials: sosecrets can be used to securely store sensitive information such as API keys, passwords, and other credentials that are required for authentication or authorization in an application.

Handling personal identifiable information (PII): sosecrets can be used to protect personal identifiable information (PII) such as names, addresses, social security numbers, and other sensitive data that needs to be kept confidential.

## API Reference

### `Secret`

The `Secret` class encapsulates a secret value and only exposes it through a controlled interface.

```
Secret(value: Optional[T] = None, func: Optional[Callable[[Any], T]] = None, func_args: Tuple[Any] = tuple(), func_kwargs: Dict[str, Any] = dict()) -> SecretType
```

- `value`: The secret value to encapsulate.
- `func`: A function to generate the secret value.
- `func_args`: The positional arguments to pass to the `func` function.
- `func_kwargs`: The keyword arguments to pass to the `func` function.

#### `apply`

The `apply` method applies a function to the secret value while keeping it encapsulated.

```python
apply(self, func: Callable[[Any], Any], *args: Tuple[Any], **kwargs: Dict[str, Any]) -> SecretType:
```

- `func`: The function to apply to the secret value.
- `args`: The positional arguments to pass to the `func` function.
- `kwargs`: The keyword arguments to pass to the `func` function.

#### `expose_secret`

The `expose_secret` method returns the value of the secret.

```python
def expose_secret(self) -> T:
```

### Exceptions

`sosecrets` defines the following exceptions:

#### `CannotInstantiateExposeSecret`

Raised when attempting to instantiate the `__expose_secret__` class.

#### `CannotInheritFromSecret`

Raised when attempting to subclass the `Secret` class.

#### `FuncAndValueCannotBeBothPassed`

Raised when both `value` and `func` arguments are passed to the `Secret` constructor.

## Contributing

Contributions are welcome! Let me know if you need help with anything else.