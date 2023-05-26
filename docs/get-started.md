## Get Started

To get started with `sosecrets`, you can follow the example below:

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

You can also refer to the [API documentation](./api.md) for more information on the available methods and classes.