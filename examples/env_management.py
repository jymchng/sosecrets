from pathlib import Path
import src
from src.sosecrets.secretdicts import ImmutableSecretMapping
from dotenv import dotenv_values

# Define the path to the `.env` file
THIS_SCRIPT_FILE_PATH = Path(__file__)
EXAMPLES = THIS_SCRIPT_FILE_PATH.parent / '.env'

# Load the environment variables and store them securely
secret_env_dict = ImmutableSecretMapping.from_func(
    dotenv_values, dotenv_path=EXAMPLES)

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
