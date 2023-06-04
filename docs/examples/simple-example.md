## Examples

Here is a simple example of how to use `sosecrets`:

### Creating a secret value

```python
from sosecrets import Secret

# Create a secret value
secret_value = Secret("my secret value")
```

### Using the secret value

```python
# Use the secret value while keeping it encapsulated
result = secret_value.apply(len)
print(result.expose_secret())  # Output: 14
```

### Retrieving the secret value

```python
# Get the value of the secret
value = secret_value.expose_secret()
print(value)  # Output: "my secret value"
```