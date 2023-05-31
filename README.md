# sosecrets

`sosecrets` is a Python module that provides a secure way to handle sensitive data by encapsulating it and only exposing it through a controlled interface.

Version: 0.1.9

[Documentation](https://sosecrets.readthedocs.io/en/latest/)

## Installation

To install `sosecrets`, you can use pip:

```bash
pip install sosecrets
```

## Usage

Here's are the examples of how to use `sosecrets`:

### Secret

Here's an example of how to use `Secret`:

```python
from sosecrets import Secret

# Create a secret value
secret_value = Secret("my secret value")

# Use the secret value while keeping it encapsulated
result: Secret[T] = secret_value.apply(len)
print(result.expose_secret())  # Output: 14

# Get the value of the secret
value = secret_value.expose_secret()
print(value)  # Output: "my secret value"
```

In this example, we create a `Secret` object with the value "my secret value". We then use the `apply` method to apply the `len` function to the secret value while keeping it encapsulated. Finally, we use the `expose_secret` method to retrieve the value of the secret.

### ImmutableSecretMapping

Here's an example of how to use `ImmutableSecretMapping`:

```python
from pathlib import Path
from sosecrets import ImmutableSecretMapping
from dotenv import dotenv_values

# Define the path to the `.env` file
THIS_SCRIPT_FILE_PATH = Path(__file__)
EXAMPLES = THIS_SCRIPT_FILE_PATH.parent / '.env'

# Load the environment variables and store them securely
secret_env_dict = ImmutableSecretMapping.from_func(dotenv_values, dotenv_path=EXAMPLES)

# Get a dictionary of the exposed values of the secret variables
exposed_dict = secret_env_dict.expose_dict()
print("exposed_dict: ", exposed_dict)

# Print the `ImmutableSecretMapping` object itself
print("secret_env_dict: ", secret_env_dict)

# Get the value associated with a key using the `get()` method
value0 = secret_env_dict.get('value0')
print("value0: ", value0)

# Get the exposed value of a key using the `get_exposed()` method
value1 = secret_env_dict.get_exposed('value1')
print("value1: ", value1)
```

The example code does the following:

1. Imports the necessary packages: `Path` from `pathlib`, `src` from the `sosecrets` module, `ImmutableSecretMapping` from `secretdicts` in the `sosecrets` module, and `dotenv_values` from the `dotenv` package.
2. Defines the path to a `.env` file that contains environment variables to be loaded.
3. Uses `ImmutableSecretMapping.from_func(dotenv_values, dotenv_path=EXAMPLES)` to load the environment variables from the `.env` file and store them in an instance of `ImmutableSecretMapping`.
4. Prints the exposed dictionary of the `ImmutableSecretMapping` object using the `expose_dict()` method.
5. Prints the `ImmutableSecretMapping` object itself.
6. Gets a value from the `ImmutableSecretMapping` object using the `get()` method and prints it.
7. Gets the exposed value of a key using the `get_exposed()` method

### MutableSecretMapping

Similar to `ImmutableSecretMapping`.

## Use Cases
sosecrets can be used in a variety of scenarios where sensitive data needs to be securely handled. Here are some common use cases:

Storing API keys, passwords, and other credentials: sosecrets can be used to securely store sensitive information such as API keys, passwords, and other credentials that are required for authentication or authorization in an application.

Handling personal identifiable information (PII): sosecrets can be used to protect personal identifiable information (PII) such as names, addresses, social security numbers, and other sensitive data that needs to be kept confidential.

## API Reference

### `Secret`

The `Secret` class encapsulates a secret value and only exposes it through a controlled interface.

```
Secret(value: Optional[T] = None, func: Optional[Callable[..., T]] = None, func_args: Tuple[Any, ...] = tuple(), func_kwargs: Dict[str, Any] = dict()) -> Secret
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

## Contributing

Contributions are welcome! Let me know if you need help with anything else.