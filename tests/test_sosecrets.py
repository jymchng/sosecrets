import pytest
from src.sosecrets import Secret
from src.sosecrets.secrets import __expose_secret__, __inner_secret__
from src.sosecrets.exceptions import CannotInheritFromSecret, FuncAndValueCannotBeBothPassed, CannotInstantiateExposeSecret


def generate_secret():
    return 'BIG SECRET'


def encrypt(value, pos_a, pos_b, kw_a=None, kw_b=None):
    return "secret_key" + ' encrypted' + pos_a + pos_b + kw_a + kw_b


def init_encrypt(pos_a, pos_b, kw_a=None, kw_b=None):
    return "secret_key" + ' encrypted' + pos_a + pos_b + kw_a + kw_b


def apply_stmt(value: str, stmt, stmt_kw=None):
    value = value.lower()
    value += stmt
    value += stmt_kw
    return value


def split_swap_join(value, stmt, stmt_kw=None):
    value = value.split(" ")
    value[1], value[0] = value[0], value[1]
    value = " ".join(value)
    value += stmt
    value += stmt_kw
    return value


@pytest.fixture
def secret_one():
    return Secret("Hello World!")


@pytest.fixture
def secret_two():
    return Secret(func=generate_secret)


def test_expose_secret(secret_one):
    assert secret_one.expose_secret(
    ) == "Hello World!", "exposed_secret={} != 'Hello World!'".format(secret_one.expose_secret())


def test_isinstance(secret_one):
    assert isinstance(secret_one, Secret)


def test_inspection_does_not_reveal_secret(secret_one):
    import inspect

    exposed_secret = secret_one.expose_secret()
    members_inspection = inspect.getmembers(secret_one)

    with pytest.raises(AttributeError):
        secret_one.__dict__

    for name, value in members_inspection:
        assert secret_one.expose_secret() != name and secret_one.expose_secret() != value


def test_initialization_with_func(secret_two):
    assert secret_two.expose_secret() == "BIG SECRET"


def test_apply(secret_one):
    assert secret_one.apply(
        apply_stmt,
        'byebye',
        stmt_kw='woah').expose_secret() == "hello world!byebyewoah"


def test_apply_two(secret_two):
    assert secret_two.apply(
        split_swap_join,
        'byebye',
        stmt_kw='woah').expose_secret() == "SECRET BIGbyebyewoah"


def test_after_application_still_secret(secret_one):
    applied_secret = secret_one.apply(apply_stmt, 'byebye', stmt_kw='woah')
    assert isinstance(applied_secret, Secret)
    assert not (applied_secret == "hello world!byebyewoah")


def test_cannot_be_inherited():
    with pytest.raises(CannotInheritFromSecret):
        class ChildSecret(Secret):
            pass


def test_func_value_cannot_be_both_passed_to_initialization():
    with pytest.raises(FuncAndValueCannotBeBothPassed):
        Secret("hello", func=encrypt)


def test_initialized_with_func():
    assert Secret(func=init_encrypt, func_args=('hello', 'bye'), func_kwargs=dict(
        kw_a='gg', kw_b='bb')).expose_secret() == "secret_key encryptedhellobyeggbb"


def test_expose_secret_cannot_be_initialized():
    with pytest.raises(CannotInstantiateExposeSecret):
        __expose_secret__()


def test_calling_from_class_raises(secret_one):
    with pytest.raises(TypeError):
        __inner_secret__.expose_secret(secret_one)
        

def test_will_not_mixed_up():
    a = Secret("Hello"); b = Secret("Bye")
    assert a.expose_secret(), b.expose_secret() == ('Hello', 'Bye')


def test_cannot_access_secret_from_class(secret_one):
    with pytest.raises(AttributeError):
        Secret.expose_secret(secret_one)
    
    
def test_secret_cannot_be_found_in_globals(secret_one):
    for k, v in secret_one.expose_secret.__globals__.items():
        assert secret_one != v