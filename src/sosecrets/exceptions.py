class CannotInheritFromSecret(Exception):

    def __str__(self):
        return "`Secret` is not inheritable, use Composition instead"


class FuncAndValueCannotBeBothPassed(Exception):

    def __str__(self) -> str:
        return "`Secret` cannot be initialized with both `value` positional argument and `func` keyword"


class CannotInstantiateExposeSecret(Exception):

    def __str__(self) -> str:
        return "Cannot instantiate `__expose_secret__` class"
