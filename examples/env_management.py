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
print("exposed_dict =", exposed_dict)

# Output
# exposed_dict = {
#     'value0': '3c976b3c66a2aa1d440d3ad99a9653c7',
#     'value1': '8f7047cda0532a374dbc380edad96c25',
#     'value2': '2e3036262c4c145c2eec97be63710ca1',
#     'value3': 'a0a514493390701d85205eaf5157602c',
#     'value4': 'c7bb1897669918c596d419ce5287fc2c',
#     'value5': '6432002518a7717456f981f550dcdad2',
#     'value6': '38e5933439295f552896d01e715dfaaf',
#     'value7': 'f657f6a409dbeac2199d49c837d259bd',
#     'value8': '62aad9acb342ad9949171b254e30b863',
#     'value9': '4d33cbecc5a8807523e4ecf44fd354c6',
#     'value10': 'aec076c60ba650bcdbceee20d9d71da7',
#     'value11': 'cef5f5f2e595a87e6ef1144887434a95',
#     'value12': 'f89955dc25aaa0fd9e1e90aa8e910410',
#     'value13': 'fa19468f8a72eb7aa871ea7e78e1960b',
#     'value14': '277103129cbf6050b7cbd6502eca9810'}

# Print the `ImmutableSecretMapping` object itself
print("secret_env_dict = ", secret_env_dict)

# Output
# secret_env_dict =  {'value0': <secrets.Secret object at 0x000002210A017540>, 
#                     'value1': <secrets.Secret object at 0x000002210A017580>, 
#                     'value2': <secrets.Secret object at 0x000002210A0175C0>, 
#                     'value3': <secrets.Secret object at 0x000002210A017600>,
#                     'value4': <secrets.Secret object at 0x000002210A017640>, 
#                     'value5': <secrets.Secret object at 0x000002210A017680>, 
#                     'value6': <secrets.Secret object at 0x000002210A0176C0>,
#                     'value7': <secrets.Secret object at 0x000002210A017700>, 
#                     'value8': <secrets.Secret object at 0x000002210A017740>, 
#                     'value9': <secrets.Secret object at 0x000002210A017780>, 
#                     'value10': <secrets.Secret object at 0x000002210A0177C0>,
#                     'value11': <secrets.Secret object at 0x000002210A017800>,
#                     'value12': <secrets.Secret object at 0x000002210A017840>,
#                     'value13': <secrets.Secret object at 0x000002210A017880>,
#                     'value14': <secrets.Secret object at 0x000002210A0178C0>}

# Get the value associated with a key using the `get()` method
value0 = secret_env_dict.get('value0')
print("value0 =", value0)

# Output
# value0 = <secrets.Secret object at 0x000002210A017540>

# Get the exposed value of a key using the `get_exposed()` method
value1 = secret_env_dict.get_exposed('value1')
print("value1 =", value1)

# Output
# value1 = 8f7047cda0532a374dbc380edad96c25
