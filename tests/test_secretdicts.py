import pytest
from typing import Dict
from secrets import token_hex
from src.sosecrets.secretdicts import ImmutableSecretMapping, MutableSecretMapping
from src.sosecrets.secrets import Secret


# Helper function to create a dictionary with random secret values
def create_secret_dict(size: int) -> Dict[str, str]:
    return {f"key{i}": token_hex(16) for i in range(size)}


# Tests for ImmutableSecretMapping class

def test_immutable_secret_mapping_init_with_empty_dict():
    with pytest.raises(ValueError):
        ImmutableSecretMapping({})


def test_immutable_secret_mapping_get_exposed():
    dict_with_secrets = create_secret_dict(10)
    immutable_mapping = ImmutableSecretMapping(
        {k: Secret(v) for k, v in dict_with_secrets.items()})
    for key in dict_with_secrets.keys():
        assert immutable_mapping.get_exposed(key) == dict_with_secrets[key]


def test_immutable_secret_mapping_get_exposed_with_default():
    dict_with_secrets = create_secret_dict(10)
    immutable_mapping = ImmutableSecretMapping(
        {k: Secret(v) for k, v in dict_with_secrets.items()})
    assert immutable_mapping.get_exposed(
        "nonexistent_key", "default_value") == "default_value"


def test_immutable_secret_mapping_from_func_with_empty_dict():
    with pytest.raises(ValueError):
        ImmutableSecretMapping.from_func(lambda: {})


def test_immutable_secret_mapping_from_func_get_exposed():
    dict_with_secrets = create_secret_dict(10)
    def func_with_secret_dict(): return dict_with_secrets
    immutable_mapping = ImmutableSecretMapping.from_func(func_with_secret_dict)
    for key in dict_with_secrets.keys():
        assert immutable_mapping.get_exposed(key) == dict_with_secrets[key]


def test_immutable_secret_mapping_from_func_get_exposed_with_default():
    dict_with_secrets = create_secret_dict(10)
    def func_with_secret_dict(): return dict_with_secrets
    immutable_mapping = ImmutableSecretMapping.from_func(func_with_secret_dict)
    assert immutable_mapping.get_exposed(
        "nonexistent_key", "default_value") == "default_value"


def test_immutable_secret_mapping_from_func_with_secret_class():
    dict_with_secrets = create_secret_dict(10)
    def func_with_secret_dict(): return {
        k: Secret(v) for k, v in dict_with_secrets.items()}
    immutable_mapping = ImmutableSecretMapping.from_func(func_with_secret_dict)
    for key in immutable_mapping.keys():
        assert immutable_mapping[key].expose_secret() == dict_with_secrets[key]


def test_immutable_secret_mapping_from_func_with_secret_class_get_exposed():
    dict_with_secrets = create_secret_dict(10)
    def func_with_secret_dict(): return {
        k: Secret(v) for k, v in dict_with_secrets.items()}
    immutable_mapping = ImmutableSecretMapping.from_func(func_with_secret_dict)
    for key in dict_with_secrets.keys():
        assert immutable_mapping.get_exposed(key) == dict_with_secrets[key]


def test_immutable_secret_mapping_from_func_with_secret_class_get_exposed_with_default():
    dict_with_secrets = create_secret_dict(10)
    def func_with_secret_dict(): return {
        k: Secret(v) for k, v in dict_with_secrets.items()}
    immutable_mapping = ImmutableSecretMapping.from_func(func_with_secret_dict)
    assert immutable_mapping.get_exposed(
        "nonexistent_key", "default_value") == "default_value"


def test_immutable_secret_mapping_from_func_with_empty_secret_class():
    with pytest.raises(ValueError):
        ImmutableSecretMapping.from_func(lambda: {})


def test_immutable_secret_mapping_from_func_with_invalid_secret_class():
    ImmutableSecretMapping.from_func(
        lambda: {
            "key1": Secret("value1"),
            "key2": "value2"})
