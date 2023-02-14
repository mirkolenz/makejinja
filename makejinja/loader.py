import typing as t

from jinja2 import Environment
from jinja2.ext import Extension

__all__ = [
    "AbstractLoader",
    "Environment",
    "Extension",
    "Extensions",
    "Filter",
    "Filters",
    "Global",
    "Globals",
    "Test",
    "Tests",
    "Policies",
    "MutableData",
    "Data",
]

Extensions = t.Sequence[t.Type[Extension]]
Filter = t.Callable[[t.Any], t.Any]
Filters = t.Sequence[Filter]
Global = t.Callable[..., t.Any]
Globals = t.Sequence[Global]
Test = t.Callable[..., t.Any]
Tests = t.Sequence[Test]
Policies = t.Mapping[str, t.Any]
MutableData = t.MutableMapping[str, t.Any]
Data = t.Mapping[str, t.Any]


class AbstractLoader:
    def __init__(self, *, env: Environment, data: MutableData) -> None:
        pass

    def filters(self) -> Filters:
        return []

    def globals(self) -> Globals:
        return []

    def tests(self) -> Tests:
        return []

    def policies(self) -> Policies:
        return {}

    def data(self) -> Data:
        return {}

    def extensions(self) -> Extensions:
        return []
