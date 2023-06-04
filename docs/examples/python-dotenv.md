# Example of Using ImmutableSecretMapping to Manage Environment Variables Safely

In this example, we demonstrate how to use the `ImmutableSecretMapping` class from the `sosecrets` module to manage environment variables safely.

We use the `dotenv` package to load environment variables from a file and then store them in an instance of `ImmutableSecretMapping`.

We then demonstrate how to access the secret values of the environment variables.

## The Code

```python
from pathlib import Path
import src
from src.sosecrets.secretdicts import ImmutableSecretMapping
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


The example code in the `examples` directory named `env_management.py` is a Python script that does the following:

1. Imports the necessary packages: `Path` from `pathlib`, `src` from the `sosecrets` module, `ImmutableSecretMapping` from `secretdicts` in the `sosecrets` module, and `dotenv_values` from the `dotenv` package.
2. Defines the path to a `.env` file that contains environment variables to be loaded.
3. Uses `ImmutableSecretMapping.from_func(dotenv_values, dotenv_path=EXAMPLES)` to load the environment variables from the `.env` file and store them in an instance of `ImmutableSecretMapping`.
4. Prints the exposed dictionary of the `ImmutableSecretMapping` object using the `expose_dict()` method.
5. Prints the `ImmutableSecretMapping` object itself.
6. Gets a value from the `ImmutableSecretMapping` object using the `get()` method and prints it.
7. Gets the exposed value of a key using the `get_exposed()` method## The Output

When the example code is run, the following output is produced:

```
exposed_dict: {
    'value0': '3c976b3c66a2aa1d440d3ad99a9653c7',
    'value1': '8f7047cda0532a374dbc380edad96c25',
    'value2': '2e3036262c4c145c2eec97be63710ca1',
    'value3': 'a0a514493390701d85205eaf5157602c',
    'value4': 'c7bb1897669918c596d419ce5287fc2c',
    'value5': '6432002518a7717456f981f550dcdad2',
    'value6': '38e5933439295f552896d01e715dfaaf',
    'value7': 'f657f6a409dbeac2199d49c837d259bd',
    'value8': '62aad9acb342ad9949171b254e30b863',
    'value9': '4d33cbecc5a8807523e4ecf44fd354c6',
    'value10': 'aec076c60ba650bcdbceee20d9d71da7',
    'value11': 'cef5f5f2e595a87e6ef1144887434a95',
    'value12': 'f89955dc25aaa0fd9e1e90aa8e910410',
    'value13': 'fa19468f8a72eb7aa871ea7e78e1960b',
    'value14': '277103129cbf6050b7cbd6502eca9810'
}

secret_env_dict =  {'value0': <secrets.Secret object at 0x000002210A017540>, 
                    'value1': <secrets.Secret object at 0x000002210A017580>, 
                    'value2': <secrets.Secret object at 0x000002210A0175C0>, 
                    'value3': <secrets.Secret object at 0x000002210A017600>,
                    'value4': <secrets.Secret object at 0x000002210A017640>, 
                    'value5': <secrets.Secret object at 0x000002210A017680>, 
                    'value6': <secrets.Secret object at 0x000002210A0176C0>,
                    'value7': <secrets.Secret object at 0x000002210A017700>, 
                    'value8': <secrets.Secret object at 0x000002210A017740>, 
                    'value9': <secrets.Secret object at 0x000002210A017780>, 
                    'value10': <secrets.Secret object at 0x000002210A0177C0>,
                    'value11': <secrets.Secret object at 0x000002210A017800>,
                    'value12': <secrets.Secret object at 0x000002210A017840>,
                    'value13': <secrets.Secret object at 0x000002210A017880>,
                    'value14': <secrets.Secret object at 0x000002210A0178C0>}

value0 = <secrets.Secret object at 0x000002210A017540>

value1 = 8f7047cda0532a374dbc380edad96c25
```

## Discussion

The `ImmutableSecretMapping` class is a dictionary-like object that stores secret values and provides methods for accessing and manipulating them. In this example, we demonstrate how to use `ImmutableSecretMapping` to manage environment variables safely by combining it with the `dotenv` package.

The `dotenv` package is a Python package that loads environment variables from a file called `.env` in the current directory. The `dotenv_values()` function from the package loads the environment variables from the file and returns them as a dictionary.

In this example, we use the `dotenv_values()` function to load the environment variables from the `.env` file and then pass them to the `ImmutableSecretMapping.from_func()` method to create an instance of `ImmutableSecretMapping`. The `from_func()` method takes a function that returns a dictionary and any additional arguments that should be passed to the function. In this case, we pass `dotenv_values` as the function argument and the path to the `.env` file as an additional argument.

Once we have an instance of `ImmutableSecretMapping`, we can use the `expose_dict()` method to get a dictionary of the exposed values of the secret variables. This method returns a new dictionary that has the same keys as the `ImmutableSecretMapping` object, but with the values replaced by their exposed values. In other words, the resulting dictionary does not contain any `Secret` objects.

We can also use the `get()` method to get a value from the `ImmutableSecretMapping` object, but this will return a `Secret` object instead of the actual value. To get the exposed value of a key, we can use the `get_exposed()` method, which returns the exposed value of the key if it exists in the `ImmutableSecretMapping` object.

It's worth noting that the `ImmutableSecretMapping` class is immutable, which means that once it is created, it cannot be modified. This is important for security reasons because it prevents any accidental or malicious modifications to the secret values stored in the object. If you need to modify the secret values, you can use the `MutableSecretMapping` class instead, which allows changes to be made to the underlying dictionary.

Overall, using `ImmutableSecretMapping` and `MutableSecretMapping` classes from the `sosecrets` module provides a convenient and secure way to manage secret values in a dictionary-like object, ensuring that sensitive information is not exposed in unintended ways.