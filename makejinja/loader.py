import typing as t

from jinja2 import Environment
from jinja2.ext import Extension

__all__ = (
    "AbstractLoader",
    "Environment",
    "Extension",
    "Extensions",
    "Filter",
    "Filters",
    "Function",
    "Functions",
    "Test",
    "Tests",
    "Policies",
    "MutableData",
    "Data",
)

Extensions = t.Sequence[type[Extension]]
Filter = t.Callable[[t.Any], t.Any]
Filters = t.Sequence[Filter]
Function = t.Callable[..., t.Any]
Functions = t.Sequence[Function]
Test = t.Callable[..., t.Any]
Tests = t.Sequence[Test]
Policies = t.Mapping[str, t.Any]
MutableData = t.MutableMapping[str, t.Any]
Data = t.Mapping[str, t.Any]


class AbstractLoader:
    def __init__(self, *, env: Environment, data: MutableData) -> None:
        pass

    def functions(self) -> Functions:
        return []

    def data(self) -> Data:
        return {}

    def filters(self) -> Filters:
        return []

    def tests(self) -> Tests:
        return []

    def policies(self) -> Policies:
        return {}

    def extensions(self) -> Extensions:
        return []

    # Deprecated: Use functions() and data() instead
    def globals(self) -> Functions:
        return []
