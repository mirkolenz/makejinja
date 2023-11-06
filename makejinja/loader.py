from collections.abc import Callable, Mapping, MutableMapping, Sequence
from typing import Any

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

Extensions = Sequence[type[Extension]]
Filter = Callable[[Any], Any]
Filters = Sequence[Filter]
Function = Callable[..., Any]
Functions = Sequence[Function]
Test = Callable[..., Any]
Tests = Sequence[Test]
Policies = Mapping[str, Any]
MutableData = MutableMapping[str, Any]
Data = Mapping[str, Any]


class AbstractLoader:
    def __init__(self, *, env: Environment, data: Data) -> None:
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
