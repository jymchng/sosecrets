import pytest
from typing import Dict
from secrets import token_hex
from src.sosecrets.secretdicts import ImmutableSecretMapping, MutableSecretMapping
from sosecrets_core.secrets import Secret


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

# Test __new__ method
def test_new_empty_mapping():
    mapping = {}
    secret_mapping = MutableSecretMapping(mapping)
    assert isinstance(secret_mapping, MutableSecretMapping)
    assert len(secret_mapping) == 0

def test_new_with_secrets():
    mapping = {"key1": Secret("secret1"), "key2": Secret("secret2")}
    secret_mapping = MutableSecretMapping(mapping)
    assert isinstance(secret_mapping, MutableSecretMapping)
    assert len(secret_mapping) == 2
    assert secret_mapping["key1"].expose_secret() == Secret("secret1").expose_secret()
    assert secret_mapping["key2"].expose_secret() == Secret("secret2").expose_secret()

def test_new_with_non_secrets():
    mapping = {"key1": "value1", "key2": "value2"}
    secret_mapping = MutableSecretMapping(mapping)
    assert isinstance(secret_mapping, MutableSecretMapping)
    assert len(secret_mapping) == 2
    assert isinstance(secret_mapping["key1"], Secret)
    assert isinstance(secret_mapping["key2"], Secret)
    assert secret_mapping["key1"].expose_secret() == "value1"
    assert secret_mapping["key2"].expose_secret() == "value2"

# Test __setitem__ method
def test_set_item_with_secret():
    secret_mapping = MutableSecretMapping({})
    secret_mapping["key"] = Secret("secret")
    assert len(secret_mapping) == 1
    assert secret_mapping["key"].expose_secret() == Secret("secret").expose_secret()

def test_set_item_with_non_secret():
    secret_mapping = MutableSecretMapping({})
    with pytest.raises(ValueError):
        secret_mapping["key"] = "value"

# Test from_func method
def func():
    return {"key": Secret("secret")}

def test_from_func_with_secrets():
    secret_mapping = MutableSecretMapping.from_func(func)
    assert len(secret_mapping) == 1
    assert secret_mapping["key"].expose_secret() == Secret("secret").expose_secret()

def test_from_func_with_non_secrets():
    def func():
        return {"key": "value"}
    
    secret_mapping = MutableSecretMapping.from_func(func)
    assert len(secret_mapping) == 1
    assert isinstance(secret_mapping["key"], Secret)
    assert secret_mapping["key"].expose_secret() == "value"

def test_from_func_empty_result():
    def func():
        return {}
    
    with pytest.raises(ValueError):
        MutableSecretMapping.from_func(func)

# Test get_exposed method
def test_get_exposed_existing_key():
    secret_mapping = MutableSecretMapping({"key": Secret("secret")})
    exposed_value = secret_mapping.get_exposed("key")
    assert exposed_value == "secret"

def test_get_exposed_missing_key():
    secret_mapping = MutableSecretMapping({})
    default_value = "default"
    exposed_value = secret_mapping.get_exposed("key", default_value)
    assert exposed_value == default_value

# Test expose_dict method
def test_expose_dict_with_secrets():
    mapping = {"key1": Secret("secret1"), "key2": Secret("secret2")}
    secret_mapping = MutableSecretMapping(mapping)
    exposed_dict = secret_mapping.expose_dict()
    assert len(exposed_dict) == 2
    assert exposed_dict["key1"] == "secret1"
    assert exposed_dict["key2"] == "secret2"
    
def test_expose_dict_with_non_secrets():
    mapping = {"key1": Secret("secret1"), "key2": "value2"}
    secret_mapping = MutableSecretMapping(mapping)
    exposed_dict = secret_mapping.expose_dict()
    assert len(exposed_dict) == 2
    assert exposed_dict["key1"] == "secret1"
    assert exposed_dict["key2"] == "value2"